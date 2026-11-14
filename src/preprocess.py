import pandas as pd
import os

def process_sales_data(input_path="data/sales.csv", output_path="data/sales_clean.csv"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo não encontrado em {input_path}. Certifique-se de colocar a planilha base.")
    
    # Leitura do CSV
    df = pd.read_csv(input_path)
    
    # Limpeza básica
    df = df.drop_duplicates()
    
    # Padronização de colunas e texto
    if 'status' in df.columns:
        df['status'] = df['status'].astype(str).str.strip().str.capitalize()
    if 'categoria' in df.columns:
        df['categoria'] = df['categoria'].astype(str).str.strip().str.title()
        
    # Conversão de data
    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df['mes_ano'] = df['data'].dt.to_period('M').astype(str)
        
    # Cálculo da Receita por linha (quantidade * preco_unitario)
    if 'quantidade' in df.columns and 'preco_unitario' in df.columns:
        df['receita'] = df['quantidade'] * df['preco_unitario']
        
    # Salvar arquivo processado (separador ';' e decimal ',')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=';', decimal=',', index=False)
    print(f"Dados limpos e salvos com sucesso em {output_path}")
    return df

def load_clean_data(path="data/sales_clean.csv"):
    if not os.path.exists(path):
        return process_sales_data()
    return pd.read_csv(path, sep=';', decimal=',')
