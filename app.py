import streamlit as st
import plotly.express as px
from src.preprocess import load_clean_data
from src.metrics import (
    get_total_revenue,
    get_total_orders,
    get_average_ticket,
    get_unique_clients,
    get_cancellation_rate,
    get_arpu,
    filter_completed
)
from src.agent import run_agent_chat

st.set_page_config(
    page_title="Data Pilot | Análise Inteligente",
    page_icon="🚀",
    layout="wide"
)

# Carregamento de dados
@st.cache_data
def get_data():
    return load_clean_data()

df = get_data()

# --- SIDEBAR ---
st.sidebar.title("🚀 Data Pilot")
st.sidebar.markdown("Painel de Vendas & Chat com Agente de IA")
st.sidebar.markdown("---")

# Filtro de Categoria
categorias = ["Todas"] + sorted(df['categoria'].dropna().unique().tolist()) if 'categoria' in df.columns else ["Todas"]
categoria_selecionada = st.sidebar.selectbox("Filtrar por Categoria", categorias)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica no Chat:** Pergunte sobre receita, ticket médio, clientes únicos, taxa de cancelamento, ARPU ou top cidades em português!")

# --- CORPO PRINCIPAL ---
st.title("📊 Painel Executivo de Vendas")
st.markdown(f"Exibindo métricas consolidadas {'para a categoria: **' + categoria_selecionada + '**' if categoria_selecionada != 'Todas' else 'geral'}.")

# Cálculo dos Cards
rev = get_total_revenue(df, categoria_selecionada)
ord_cnt = get_total_orders(df, categoria_selecionada)
tkt = get_average_ticket(df, categoria_selecionada)
cli = get_unique_clients(df, categoria_selecionada)
arpu = get_arpu(df, categoria_selecionada)
canc_rate = get_cancellation_rate(df)

# Exibição em Cards (Métricas)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Receita Total", f"R$ {rev:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Pedidos Concluídos", f"{ord_cnt:,}")
col3.metric("Ticket Médio", f"R$ {tkt:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col4.metric("Clientes Únicos", f"{cli:,}")
col5.metric("ARPU (Receita/Cliente)", f"R$ {arpu:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- GRÁFICOS (Plotly) ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📈 Evolução da Receita Mensal")
    df_comp = filter_completed(df)
    if categoria_selecionada != "Todas":
        df_comp = df_comp[df_comp['categoria'] == categoria_selecionada]
    
    if 'mes_ano' in df_comp.columns and not df_comp.empty:
        df_mensal = df_comp.groupby('mes_ano')['receita'].sum().reset_index()
        fig_mensal = px.line(df_mensal, x='mes_ano', y='receita', markers=True, 
                             labels={'mes_ano': 'Mês/Ano', 'receita': 'Receita (R$)'})
        fig_mensal.update_layout(template="plotly_dark", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_mensal, use_container_width=True)
    else:
        st.info("Sem dados temporais disponíveis.")

with col_g2:
    st.subheader("🏙️ Top 5 Cidades em Vendas (Melhoria)")
    if 'cidade' in df_comp.columns and not df_comp.empty:
        df_cidade = df_comp.groupby('cidade')['receita'].sum().reset_index()
        df_cidade = df_cidade.sort_values(by='receita', ascending=False).head(5)
        fig_cidade = px.bar(df_cidade, x='cidade', y='receita', text_auto='.2s',
                            labels={'cidade': 'Cidade', 'receita': 'Receita (R$)'})
        fig_cidade.update_layout(template="plotly_dark", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_cidade, use_container_width=True)
    else:
        st.info("Sem dados de cidades disponíveis.")

st.markdown("---")

# --- CHAT INTELIGENTE COM AGENTE ---
st.subheader("💬 Conversa com os Dados (Data Pilot Agent)")
st.markdown("Faça perguntas em linguagem natural sobre o seu negócio:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: Qual foi a receita total da categoria Eletrônicos? Ou quais são as top cidades?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("O agente está consultando as funções Python..."):
            response_text = run_agent_chat(prompt, df)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
