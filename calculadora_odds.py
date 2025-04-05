import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração
st.set_page_config(page_title="Calculadora PRO", page_icon="✅", layout="centered")

# Funções
def calcular_odds(odd, minuto, descontos, tempo_total):
    minutos_restantes = tempo_total + descontos - minuto
    reducao_por_minuto = (odd - 1) / minutos_restantes if minutos_restantes > 0 else 0
    return [
        (minuto + i, max(1.0, odd - reducao_por_minuto * i))
        for i in range(minutos_restantes + 1)
    ]

# Interface
st.title("⚽ Calculadora de Odds Dinâmica")
with st.sidebar:
    st.header("Configurações")
    mercado = st.selectbox("Mercado:", ["1° Tempo (45min)", "2° Tempo (45min)", "Tempo Integral (90min)"])
    odd = st.number_input("Odd Atual:", min_value=1.01, value=2.5, step=0.1)
    minuto = st.slider("Minuto Atual:", 0, 90, 15)
    descontos = st.slider("Acréscimos (min):", 0, 15, 3)

# Processamento
tempo_regulamentar = 45 if "Tempo" in mercado else 90
if st.button("Calcular", type="primary"):
    dados = calcular_odds(odd, minuto, descontos, tempo_regulamentar)
    df = pd.DataFrame(dados, columns=["Minuto", "Odd"])
    
    # Gráfico
    fig = px.line(df, x="Minuto", y="Odd", title="Projeção da Odd")
    st.plotly_chart(fig)
    
    # Tabela
    st.dataframe(
        df.style.highlight_max(axis=0, color="#FFFD75")
              .format({"Odd": "{:.3f}"}),
        height=400
    )

st.markdown("---")
st.caption("App desenvolvido com Streamlit | Atualização automática")