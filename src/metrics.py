import pandas as pd

def filter_completed(df):
    if 'status' in df.columns:
        return df[df['status'].str.lower() == 'concluído']
    return df

def get_total_revenue(df, categoria=None):
    df_filtered = filter_completed(df)
    if categoria and categoria != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == categoria]
    return float(df_filtered['receita'].sum())

def get_total_orders(df, categoria=None):
    df_filtered = filter_completed(df)
    if categoria and categoria != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == categoria]
    return int(df_filtered['id_pedido'].nunique() if 'id_pedido' in df_filtered.columns else len(df_filtered))

def get_average_ticket(df, categoria=None):
    df_filtered = filter_completed(df)
    if categoria and categoria != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == categoria]
    orders = get_total_orders(df_filtered)
    revenue = get_total_revenue(df_filtered)
    return float(revenue / orders) if orders > 0 else 0.0

def get_unique_clients(df, categoria=None):
    df_filtered = filter_completed(df)
    if categoria and categoria != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == categoria]
    return int(df_filtered['id_cliente'].nunique() if 'id_cliente' in df_filtered.columns else 0)

def get_cancellation_rate(df):
    if 'status' not in df.columns or len(df) == 0:
        return 0.0
    total = len(df)
    canceled = len(df[df['status'].str.lower() == 'cancelado'])
    return float((canceled / total) * 100)

# --- MELHORIAS IMPLEMENTADAS ---
def get_arpu(df, categoria=None):
    """Métrica Nova: Receita Média por Cliente (ARPU)"""
    revenue = get_total_revenue(df, categoria)
    clients = get_unique_clients(df, categoria)
    return float(revenue / clients) if clients > 0 else 0.0

def get_top_cities(df, top_n=5):
    """Ferramenta/Métrica Nova: Top cidades com maior volume de vendas"""
    df_filtered = filter_completed(df)
    if 'cidade' not in df_filtered.columns:
        return "Coluna de cidade não encontrada."
    top = df_filtered.groupby('cidade')['receita'].sum().reset_index()
    top = top.sort_values(by='receita', ascending=False).head(top_n)
    return top.to_dict(orient='records')
