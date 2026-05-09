import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIGURACIÓN TÉCNICA ---
st.set_page_config(page_title="ASO Master - Sistema Automatizado", layout="wide")

# CSS para Zero-Scroll y Legibilidad
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    .block-container { padding-top: 1rem !important; }
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #fcfcfd; }
    .main-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #f1f5f9; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.04); margin-bottom: 10px; }
    .question-text { font-size: 1.8rem; font-weight: 700; color: #0f172a; line-height: 1.1; margin-bottom: 15px; }
    div.stRadio > div { flex-direction: column !important; gap: 6px; }
    label[data-baseweb="radio"] { background-color: #ffffff; padding: 12px 18px !important; border-radius: 12px !important; border: 2px solid #f1f5f9 !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE VARIABLES ---
if 'paso' not in st.session_state: st.session_state.paso = 'landing'
if 'respuestas' not in st.session_state: st.session_state.respuestas = {}
if 'organizacion' not in st.session_state: st.session_state.organizacion = ""

# --- CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- DEFINICIONES Y DIMENSIONES ---
dimensiones = {
    "Exigencias Psicológicas": {"rango": range(1, 9), "inv": []},
    "Control y Autonomía": {"rango": range(9, 17), "inv": range(9, 17)},
    "Apoyo Social y Liderazgo": {"rango": range(17, 25), "inv": range(17, 25)},
    "Recompensa y Sentido": {"rango": range(25, 33), "inv": range(25, 33)},
    "Vida Personal": {"rango": range(33, 41), "inv": [33, 36, 37, 39, 40]},
    "Loops Neuropsicológicos": {"rango": range(41, 51), "inv": []}
}

# (Cargar aquí las 50 preguntas que ya tienes definidas)
preguntas_texto = {
    1: "Siento que la velocidad exigida en mis tareas supera habitualmente mi capacidad de respuesta.",
    # ... (Pega aquí el resto de las 50 preguntas que usamos antes)
    50: "¿Te sientes emocionalmente agotado antes de interactuar con colegas?"
}

# --- 1. LANDING PAGE (Identificación de Organización) ---
if st.session_state.paso == 'landing':
    st.markdown('# Auditoría ASO Master')
    col_l, col_r = st.columns([1.5, 1], gap="medium")
    
    with col_l:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Datos de la Evaluación")
        # Aquí capturamos de dónde viene el resultado
        org_input = st.text_input("Nombre de la Organización / Institución:", 
                                 placeholder="Ej: Hospital Regional - Unidad de Trauma")
        
        st.write("Esta herramienta busca entender cómo la organización del trabajo influye en su energía y bienestar...")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_r:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        if st.button("Comenzar Evaluación", use_container_width=True, type="primary"):
            if org_input:
                st.session_state.organizacion = org_input
                st.session_state.paso = 'evaluando'
                st.rerun()
            else:
                st.error("⚠️ Ingrese el nombre de la organización para continuar.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CUESTIONARIO ---
elif st.session_state.paso == 'evaluando':
    idx = len(st.session_state.respuestas) + 1
    if idx <= 50:
        st.progress(idx / 50)
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write(f"Pregunta {idx} de 50 | Organización: {st.session_state.organizacion}")
        st.markdown(f'<p class="question-text">{preguntas_texto.get(idx, "Cargando...")}</p>', unsafe_allow_html=True)
        res = st.radio("Acuerdo:", [5, 4, 3, 2, 1], 
                       format_func=lambda x: {5:"Totalmente de acuerdo", 1:"Totalmente en desacuerdo"}.get(x, str(x)),
                       key=f"r_{idx}", label_visibility="collapsed")
        if st.button("Siguiente"):
            st.session_state.respuestas[idx] = res
            st.rerun()
    else:
        st.session_state.paso = 'reporte'
        st.rerun()

# --- 3. REPORTE Y AUTO-GUARDADO ---
elif st.session_state.paso == 'reporte':
    # Cálculos y lógica de inversión
    promedios = {}
    for nom, info in dimensiones.items():
        vals = [st.session_state.respuestas[i] for i in info["rango"]]
        vals_adj = [6 - v if i in info["inv"] else v for i, v in zip(info["rango"], vals)]
        promedios[nom] = sum(vals_adj) / len(vals_adj)

    # Hipótesis basada en punto de corte 3.5
    exig = promedios["Exigencias Psicológicas"]
    loop = promedios["Loops Neuropsicológicos"]
    hipotesis = "Saturación Sistémica" if exig >= 3.5 and loop >= 3.5 else "Estable"

    # --- GUARDADO EN EXCEL MAESTRO ---
    if 'guardado' not in st.session_state:
        # Fila de datos para la organización identificada
        new_row = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Organización": st.session_state.organizacion,
            "Exigencias": round(promedios["Exigencias Psicológicas"], 2),
            "Control": round(promedios["Control y Autonomía"], 2),
            "Apoyo": round(promedios["Apoyo Social y Liderazgo"], 2),
            "Recompensa": round(promedios["Recompensa y Sentido"], 2),
            "Vida_Personal": round(promedios["Vida Personal"], 2),
            "Loops": round(promedios["Loops Neuropsicológicos"], 2),
            "Hipotesis": hipotesis
        }])
        
        try:
            # Sincronización con Google Sheets
            existing_data = conn.read(worksheet="DB_Auditoria_ASO")
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(worksheet="DB_Auditoria_ASO", data=updated_df)
            st.session_state.guardado = True
            st.toast(f"✅ Datos de {st.session_state.organizacion} guardados.")
        except:
            st.warning("⚠️ No se pudo sincronizar con la base de datos central.")

    # (Mostrar Reporte Visual aquí...)
    st.header(f"📊 Informe: {st.session_state.organizacion}")
    # ... (Resto del código de gráficos que ya tenemos)
