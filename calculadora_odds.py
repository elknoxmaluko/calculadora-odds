import streamlit as st
import pandas as pd

# Configuração básica garantida
st.set_page_config(
    page_title="Calculadora de Odds",
    page_icon="⚽",
    layout="centered"
)

# Função de cálculo simplificada e testada
def calcular_odds(odd, minuto, descontos, tempo_total):
    minutos_restantes = tempo_total + descontos - minuto
    if minutos_restantes <= 0:
        return []
    reducao = (odd - 1) / minutos_restantes
    return [
        (minuto + i, max(1.0, odd - reducao * i))
        for i in range(minutos_restantes + 1)
    ]

# CSS mínimo garantido
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 4px;
}
.stDataFrame {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Interface simplificada
st.title("Calculadora de Odds")

with st.sidebar:
    st.header("Configurações")
    mercado = st.selectbox("Mercado", ["1° Tempo (45min)", "2° Tempo (45min)", "Tempo Total (90min)"])
    odd = st.number_input("Odd Atual", min_value=1.01, value=2.5, step=0.1)
    minuto = st.slider("Minuto Atual", 0, 90, 15)
    descontos = st.slider("Acréscimos (min)", 0, 15, 3)

# Cálculo e exibição
if st.button("Calcular"):
    tempo_total = 45 if "1°" in mercado else 90
    resultados = calcular_odds(odd, minuto, descontos, tempo_total)
    
    if not resultados:
        st.error("O minuto atual é maior que o tempo total da partida")
    else:
        df = pd.DataFrame(resultados, columns=["Minuto", "Odd"])
        st.dataframe(
            df.style.format({"Odd": "{:.3f}"})
                  .highlight_max(axis=0, color="#FFFD75"),
            height=400
        )
