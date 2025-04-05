import streamlit as st
import pandas as pd
from PIL import Image
import base64

# Configuração da página com tema personalizável
st.set_page_config(
    page_title="Calculadora PRO Odds",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS AVANÇADO COM ANIMAÇÕES ---
st.markdown("""
<style>
    :root {
        --primary: #3498db;
        --secondary: #2ecc71;
        --dark: #2c3e50;
        --light: #ecf0f1;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, var(--dark) 0%, #34495e 100%) !important;
        color: white;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4) !important;
    }
    
    .stNumberInput, .stSlider, .stSelectbox {
        margin-bottom: 1.5rem !important;
    }
    
    .stDataFrame {
        border-radius: 12px !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease;
    }
    
    .stDataFrame:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
    }
    
    .highlight-row {
        background-color: #e3f2fd !important;
        font-weight: bold !important;
    }
    
    /* Animação de entrada */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO PARA CARREGAR LOGO ---
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Logo (substitua pelo caminho da sua imagem ou use URL)
logo_html = """
<div style="text-align:center; margin-bottom:30px">
    <img src="data:image/png;base64,{}" width="180">
</div>
""".format(
    get_image_base64("logo.png")  # Substitua pelo seu arquivo ou use URL
)

# --- FUNÇÕES PRINCIPAIS ---
def calcular_odds(odd_atual, minuto_atual, descontos, tempo_total):
    minutos_restantes = tempo_total + descontos - minuto_atual
    if minutos_restantes <= 0:
        return []
    reducao_por_minuto = (odd_atual - 1.0) / minutos_restantes
    return [
        (minuto_atual + i, minuto_atual + descontos + tempo_total - (minuto_atual + i), 
         max(1.0, odd_atual - reducao_por_minuto * i))
        for i in range(minutos_restantes + 1)
    ]

# --- SIDEBAR PREMIUM ---
with st.sidebar:
    st.markdown(logo_html, unsafe_allow_html=True)
    
    # Seletor de tema
    tema = st.radio(
        "🎨 Tema Visual",
        ["Claro", "Escuro"],
        horizontal=True,
        index=0
    )
    
    st.markdown("---")
    st.header("⚙️ Configurações")
    
    mercado = st.selectbox(
        "**Mercado**", 
        ["Primeiro Tempo (45min)", "Segundo Tempo (45min)", "Tempo Integral (90min)"],
        index=2
    )
    
    odd_atual = st.number_input(
        "**Odd Atual**", 
        min_value=1.01, 
        value=2.5, 
        step=0.1,
        format="%.2f"
    )
    
    minuto_atual = st.slider(
        "**Minuto Atual**", 
        0, 90, 15,
        help="Minuto atual da partida"
    )
    
    descontos = st.slider(
        "**Acréscimos (min)**", 
        0, 15, 3,
        help="Tempo de acréscimos/jogo parado"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#bdc3c7;font-size:0.8em">
        v2.0 • Desenvolvido por você
    </div>
    """, unsafe_allow_html=True)

# --- CONTEÚDO PRINCIPAL ---
st.title("📊 Calculadora PRO de Odds")
st.markdown("""
<div class="fade-in" style="background:linear-gradient(90deg, var(--primary), var(--secondary));
            padding:16px;border-radius:12px;margin-bottom:28px;color:white;text-align:center">
    <h3 style="color:white;margin:0">Calcule a evolução das odds com precisão</h3>
</div>
""", unsafe_allow_html=True)

if st.button("🔍 Calcular Odds Automático", type="primary"):
    tempo_regulamentar = 45 if "Tempo" in mercado else 90
    resultados = calcular_odds(odd_atual, minuto_atual, descontos, tempo_regulamentar)
    
    if not resultados:
        st.error("""
        <div style='border-left:4px solid #e74c3c;padding-left:12px'>
            <h4 style='color:#e74c3c'>⛔ Atenção!</h4>
            <p>O minuto atual é maior que o tempo total da partida</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = pd.DataFrame(
            resultados, 
            columns=["Minuto", "Min. Restantes", "Odd Projetada"]
        )
        
        # Aplicando estilo condicional avançado
        def estilo_linha(row):
            styles = [''] * len(row)
            if row["Minuto"] % 5 == 0:
                styles = ['background: #e3f2fd; font-weight: bold'] * len(row)
            if row["Min. Restantes"] <= 5:
                styles = ['background: #ffebee; color: #c62828'] * len(row)
            return styles
        
        # Exibição premium dos resultados
        with st.container():
            st.success(f"""
            <div style='border-left:4px solid #2ecc71;padding-left:12px'>
                <h4 style='color:#2ecc71'>✅ Cálculo concluído!</h4>
                <p>Mercado: {mercado} | Odd Inicial: {odd_atual:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                df.style.format({"Odd Projetada": "{:.3f}"})
                      .apply(estilo_linha, axis=1)
                      .set_properties(**{
                          'text-align': 'center',
                          'font-size': '14px'
                      })
                      .set_table_styles([{
                          'selector': 'th',
                          'props': [('background', 'var(--dark)'), ('color', 'white')]
                      }]),
                height=600,
                use_container_width=True
            )

# --- RODAPÉ DINÂMICO ---
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;color:#7f8c8d">
    <div>Atualização em tempo real</div>
    <div>
        <button style="background:#3498db;color:white;border:none;padding:8px 16px;border-radius:4px">
            Exportar Dados
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SCRIPT PARA ALTERAR TEMA DINAMICAMENTE ---
st.markdown(f"""
<script>
    document.body.className = '{'dark-theme' if tema == 'Escuro' else 'light-theme'}';
</script>
""", unsafe_allow_html=True)
