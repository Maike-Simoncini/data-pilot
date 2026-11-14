import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.metrics import (
    get_total_revenue, 
    get_total_orders, 
    get_average_ticket, 
    get_unique_clients, 
    get_cancellation_rate,
    get_arpu,
    get_top_cities
)

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL_NAME = os.getenv("MODEL_NAME", "google/gemini-2.0-flash-exp:free")

# Definição das ferramentas (Tools) para o LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_total_revenue",
            "description": "Calcula a receita total de vendas para pedidos concluídos, podendo filtrar por categoria.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {"type": "string", "description": "Nome da categoria de produtos (ex: Eletrônicos, Roupas)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_orders",
            "description": "Retorna o número total de pedidos concluídos, podendo filtrar por categoria.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {"type": "string", "description": "Nome da categoria de produtos"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_average_ticket",
            "description": "Calcula o ticket médio dos pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {"type": "string", "description": "Nome da categoria de produtos"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_unique_clients",
            "description": "Retorna o número de clientes únicos que realizaram pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {"type": "string", "description": "Nome da categoria de produtos"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cancellation_rate",
            "description": "Calcula a taxa percentual de cancelamento dos pedidos na base.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_arpu",
            "description": "Calcula a receita média por cliente (ARPU) para pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {"type": "string", "description": "Nome da categoria de produtos"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_cities",
            "description": "Retorna as principais cidades em volume de vendas (receita).",
            "parameters": {
                "type": "object",
                "properties": {
                    "top_n": {"type": "integer", "description": "Número de cidades a retornar (padrão 5)"}
                },
                "required": []
            }
        }
    }
]

def run_agent_chat(user_prompt, df):
    messages = [
        {
            "role": "system",
            "content": "Você é o Data Pilot, um assistente inteligente de vendas corporativas. "
                       "Responda sempre em português de forma clara e objetiva. "
                       "Você DEVE usar as ferramentas fornecidas para calcular os números exatos. Nunca invente valores."
        },
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments or "{}")
                
                # Mapeamento de execução segura das funções
                function_mapping = {
                    "get_total_revenue": lambda: get_total_revenue(df, **function_args),
                    "get_total_orders": lambda: get_total_orders(df, **function_args),
                    "get_average_ticket": lambda: get_average_ticket(df, **function_args),
                    "get_unique_clients": lambda: get_unique_clients(df, **function_args),
                    "get_cancellation_rate": lambda: get_cancellation_rate(df),
                    "get_arpu": lambda: get_arpu(df, **function_args),
                    "get_top_cities": lambda: get_top_cities(df, **function_args)
                }
                
                if function_name in function_mapping:
                    tool_output = function_mapping[function_name]()
                else:
                    tool_output = f"Erro: Função {function_name} não encontrada."
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(tool_output)
                })
            
            second_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            return second_response.choices[0].message.content
        
        return response_message.content

    except Exception as e:
        return f"Erro ao comunicar com o OpenRouter: {str(e)}"
