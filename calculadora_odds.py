import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Odds",
    page_icon="⚽",
    layout="centered"
)

# CSS para temas (adicionado dinamicamente)
def aplicar_tema(tema):
    if tema == "Escuro":
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .stDataFrame {
                background-color: #2D2D2D !important;
                color: white !important;
            }
            .stSelectbox, .stNumberInput, .stSlider {
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: #FFFFFF;
                color: #000000;
            }
        </style>
        """, unsafe_allow_html=True)

# Função de cálculo
def calcular_odds(odd, minuto, descontos, tempo_total):
    minutos_restantes = tempo_total + descontos - minuto
    if minutos_restantes <= 0:
        return []
    reducao = (odd - 1) / minutos_restantes
    return [
        (minuto + i, max(1.0, odd - reducao * i))
        for i in range(minutos_restantes + 1)
    ]

# Sidebar com seletor de tema
with st.sidebar:
    st.header("Configurações")
    tema = st.radio("Tema", ["Claro", "Escuro"], index=0)
    aplicar_tema(tema)
    
    mercado = st.selectbox("Mercado", ["1° Tempo (45min)", "2° Tempo (45min)", "Tempo Total (90min)"])
    odd = st.number_input("Odd Atual", min_value=1.01, value=2.5, step=0.1)
    minuto = st.slider("Minuto Atual", 0, 90, 15)
    descontos = st.slider("Acréscimos (min)", 0, 15, 3)

# Interface principal
st.title("Calculadora de Odds")

if st.button("Calcular"):
    tempo_total = 45 if "1°" in mercado else 90
    resultados = calcular_odds(odd, minuto, descontos, tempo_total)
    
    if not resultados:
        st.error("O minuto atual é maior que o tempo total da partida")
    else:
        df = pd.DataFrame(resultados, columns=["Minuto", "Odd"])
        
        # Ajusta estilo da tabela conforme tema
        if tema == "Escuro":
            estilo_tabela = [{
                'selector': 'th',
                'props': [('background-color', '#2D2D2D'), ('color', 'white')]
            }]
        else:
            estilo_tabela = [{
                'selector': 'th',
                'props': [('background-color', '#f0f2f6'), ('color', 'black')]
            }]
        
        st.dataframe(
            df.style.format({"Odd": "{:.3f}"})
                  .set_table_styles(estilo_tabela),
            height=400
        )
