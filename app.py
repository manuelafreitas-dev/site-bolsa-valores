import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Hub de Investimentos", page_icon="📈", layout="wide")

# Estilização personalizada para o Modo Escuro Perfeito
st.markdown("""
    <style>
    /* Cor de fundo do site */
    .stApp { background-color: #0E1117; }
    
    /* Força todos os textos principais e títulos a ficarem brancos */
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    
    /* Deixa o tamanho da cotação grande e com uma cor azul neon bem chamativa */
    div[data-testid="stMetricValue"] { font-size: 38px; font-weight: bold; color: #4D96FF !important; }
    
    /* Altera a caixa de digitação para não ser aquele blocão branco */
    div[data-testid="stTextInput"] input {
        background-color: #1A1F2C !important;
        color: #FFFFFF !important;
        border: 1px solid #4D96FF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração do título do site
st.title("📊 Painel de Investimentos")
st.subheader("Monitore a variação das suas ações em tempo real")
col_esquerda, col_direita = st.columns(2)
with col_esquerda: 
    # Campo de busca para o usuário digitar a ação (ex: PETR4.SA para Petrobras, AAPL para Apple)
    ticker = st.text_input("Digite o código da ação (ex: PETR4.SA, VALE3.SA, AAPL):", "PETR4.SA")
with col_direita:
    if ticker:
        # Busca os dados da ação usando a API do Yahoo Finance
        acao = yf.Ticker(ticker)
        dados = acao.history(period="2d") # Pega os dados dos últimos 2 dias para calcular a variação
        
        if len(dados) >= 2:
            preco_atual = dados['Close'].iloc[-1]
            preco_anterior = dados['Close'].iloc[-2]
            
            # Calcula a variação de preço e a porcentagem
            variacao = preco_atual - preco_anterior
            porcentagem = (variacao / preco_anterior) * 100
            
            # Exibe os dados na tela com cores (verde para alta, vermelho para baixa)
            st.metric(
                label=f"Ação: {ticker.upper()}",
                value=f"R$ {preco_atual:.2f}",
                delta=f"{variacao:.2f} ({porcentagem:.2f}%)"
            )
            
            # Mostra um gráfico histórico simples dos últimos 30 dias
            st.subheader("Histórico dos últimos 30 dias")
            historico_longo = acao.history(period="30d")
            st.line_chart(historico_longo['Close'])
        else:
            st.error("Código da ação não encontrado ou dados indisponíveis.")
