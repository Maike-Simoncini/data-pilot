# 🚀 Data Pilot — Análise Inteligente de Dados com Agentes de IA

<p align="center">
  <b>Painel executivo de vendas em Python com Streamlit, Plotly e Agente de IA com Function Calling via OpenRouter.</b>
</p>

---

## 📋 Sobre o Projeto
O **Data Pilot** é uma aplicação completa desenvolvida para transformar dados brutos de vendas em inteligência acionável. O sistema é dividido em duas frentes integradas:
1. **Painel Interativo:** Cards de métricas financeiras (Receita, Pedidos, Ticket Médio, Clientes Únicos, ARPU) e gráficos dinâmicos filtráveis por categoria e localidade.
2. **Chat Inteligente com Agente:** Um assistente em linguagem natural que utiliza **Function Calling**. A regra de ouro é rigorosamente seguida: **o Python calcula com precisão matemática, e a LLM apenas interpreta e explica os resultados**, eliminando alucinações.

---

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+**
* **Pandas** (Limpeza e transformação de dados)
* **Streamlit** (Interface gráfica do painel e chat)
* **Plotly** (Visualização de gráficos interativos)
* **OpenAI SDK / OpenRouter API** (Orquestração do modelo de IA gratuito para Function Calling)

---

## 🌟 Melhorias Implementadas em Relação à Base
* **Nova Métrica (ARPU):** Cálculo da Receita Média por Cliente (`get_arpu`) integrado tanto no painel superior quanto nas ferramentas do agente.
* **Novo Gráfico (Top 5 Cidades):** Visualização em barras das cidades com maior volume de faturamento.
* **Nova Ferramenta de Chat (`get_top_cities`):** O agente agora é capaz de consultar e listar de forma autônoma as principais praças de vendas da empresa.

---

## ⚙️ Como Instalar e Executar Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/Maike-Simoncini/data-pilot.git
cd data-pilot
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Copie o arquivo de exemplo e insira sua chave do OpenRouter:
```bash
cp .env.example .env
```
Edite o `.env` com sua chave:
```env
OPENROUTER_API_KEY=sua_chave_aqui
```

### 5. Executar a Aplicação
```bash
streamlit run app.py
```

---

## 🖖 Autor
Desenvolvido por **Maike Simoncini da Silva** (`@Dev_Excelente`).  
*Long live and prosper!* 🚀
