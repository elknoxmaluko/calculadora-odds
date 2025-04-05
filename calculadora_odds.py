import streamlit as st
import pandas as pd

# Configuração da página com tema profissional
st.set_page_config(
    page_title="Odds Perfect Calculator",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS profissional com variáveis de cor
st.markdown("""
<style>
    :root {
        --primary: #4f46e5;
        --secondary: #10b981;
        --background: #f8fafc;
        --card: #ffffff;
        --text: #334155;
        --border: #e2e8f0;
    }
    
    [data-testid="stAppViewContainer"] {
        background: var(--background);
        color: var(--text);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary), #4338ca) !important;
        border-right: 1px solid var(--border);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .stNumberInput, .stSlider, .stSelectbox {
        margin-bottom: 1rem;
    }
    
    .stDataFrame {
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Títulos personalizados */
    h1 {
        color: var(--primary) !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Cards modernos */
    .custom-card {
        background: var(--card);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 1px solid var(--border);
    }
</style>
""", unsafe_allow_html=True)

# Função de cálculo otimizada
def calcular_odds(odd_atual, minuto_atual, descontos, tempo_total):
    tempo_jogo = tempo_total + descontos
    if minuto_atual >= tempo_jogo:
        return None
    
    reducao_minuto = (odd_atual - 1.0) / (tempo_jogo - minuto_atual)
    return [
        {
            "Minuto": minuto_atual + i,
            "Min. Restantes": tempo_jogo - (minuto_atual + i),
            "Odd": max(1.0, odd_atual - reducao_minuto * i)
        }
        for i in range(tempo_jogo - minuto_atual + 1)
    ]

# Sidebar profissional
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; margin-bottom:2rem'>
        <h2 style='color:white; font-weight:600'>⚙️ Configurações</h2>
    </div>
    """, unsafe_allow_html=True)
    
    mercado = st.selectbox(
        "**Selecione o Mercado**",
        ["Primeiro Tempo (45min)", "Segundo Tempo (45min)", "Tempo Integral (90min)"],
        index=2
    )
    
    odd = st.number_input(
        "**Odd Atual**",
        min_value=1.01,
        value=2.5,
        step=0.1,
        format="%.2f"
    )
    
    minuto = st.slider(
        "**Minuto Atual**",
        0, 90, 15,
        help="Minuto atual da partida"
    )
    
    descontos = st.slider(
        "**Tempo de Acréscimos**",
        0, 15, 3,
        help="Minutos adicionais no final do jogo"
    )

# Conteúdo principal premium
st.markdown("""
<div class='custom-card'>
    <h1>🎯 Calculadora Perfect Odds</h1>
    <p style='color:var(--text)'>Previsão precisa da variação das odds durante a partida</p>
</div>
""", unsafe_allow_html=True)

if st.button("🔍 Calcular Projeção", type="primary"):
    tempo_total = 45 if "Primeiro" in mercado else 90
    resultados = calcular_odds(odd, minuto, descontos, tempo_total)
    
    if resultados is None:
        st.error("""
        <div style='
            background: #fee2e2;
            color: #b91c1c;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #dc2626;
            margin: 1rem 0;
        '>
            ⚠️ O minuto atual não pode ser maior que o tempo total da partida
        </div>
        """, unsafe_allow_html=True)
    else:
        df = pd.DataFrame(resultados)
        
        st.success("""
        <div style='
            background: #ecfdf5;
            color: #065f46;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #10b981;
            margin: 1rem 0;
        '>
            ✅ Projeção calculada com sucesso!
        </div>
        """, unsafe_allow_html=True)
        
        # Formatação profissional da tabela
        st.dataframe(
            df.style.format({"Odd": "{:.3f}"})
                  .apply(lambda x: ['background: #f8fafc' if x.name % 2 == 0 else '' 
                                   for _ in x], axis=1)
                  .set_properties(**{
                      'text-align': 'center',
                      'font-size': '14px'
                  })
                  .set_table_styles([{
                      'selector': 'th',
                      'props': [
                          ('background', 'var(--primary)'),
                          ('color', 'white'),
                          ('font-weight', '600')
                      ]
                  }]),
            height=500,
            use_container_width=True
        )

# Rodapé profissional
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#64748b; font-size:0.9rem; margin-top:2rem'>
    🚀 Versão Premium • Atualização em tempo real
</div>
""", unsafe_allow_html=True)
