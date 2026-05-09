import streamlit as st
import pandas as pd
import plotly.express as px

# --- DISEÑO Y ARQUITECTURA VISUAL ---
st.set_page_config(page_title="ASO Master - Diagnóstico de Precisión", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #fcfcfd; }
    
    /* Contenedores Principales */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 28px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.03);
        margin-bottom: 25px;
    }
    
    .question-text {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
        margin-bottom: 30px;
    }
    
    .section-label {
        color: #3b82f6;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 800;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }

    .landing-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #1e3a8a;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    
    /* Botones y Radio personalizados */
    .stButton>button {
        border-radius: 15px;
        padding: 20px;
        font-weight: 700;
        background-color: #1e3a8a;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS (50 ÍTEMS) ---
dimensiones = {
    "Exigencias Psicológicas": {"rango": range(1, 9), "inv": []},
    "Control y Autonomía": {"rango": range(9, 17), "inv": range(9, 17)},
    "Apoyo Social y Liderazgo": {"rango": range(17, 25), "inv": range(17, 25)},
    "Recompensa y Sentido": {"rango": range(25, 33), "inv": range(25, 33)},
    "Vida Personal": {"rango": range(33, 41), "inv": [33, 36, 37, 39, 40]},
    "Loops Neuropsicológicos": {"rango": range(41, 51), "inv": []}
}

preguntas_texto = {
    1: "Siento que la velocidad exigida en mis tareas supera habitualmente mi capacidad de respuesta.",
    2: "La distribución de mis labores suele ser irregular, generando 'cuellos de botella'.",
    3: "El volumen de actividades pendientes me obliga a sacrificar la calidad por la rapidez.",
    4: "Mi atención se siente fragmentada por saltar constantemente de un tema a otro.",
    5: "Al finalizar el día, experimento un agotamiento mental que me impide mi vida personal.",
    6: "Percibo que las metas de mi área son poco realistas para el tiempo disponible.",
    7: "Es habitual que deba resolver urgencias externas que interrumpen mi planificación.",
    8: "La complejidad de mis funciones requiere un nivel de alerta desgastador.",
    9: "Siento que tengo un margen de decisión real sobre la organización de mi agenda.",
    10: "La institución valora e incorpora mis sugerencias para optimizar los procesos.",
    11: "Mi jefatura me otorga la confianza para resolver problemas según mi criterio.",
    12: "Tengo la oportunidad de aplicar mis habilidades de forma creativa.",
    13: "Siento que puedo influir en las decisiones que afectan mi flujo de trabajo.",
    14: "El diseño de mis tareas me permite aprender nuevas competencias.",
    15: "Percibo que los métodos de trabajo son flexibles y se adaptan a la realidad.",
    16: "Siento que mis acciones tienen un impacto visible en el éxito del departamento.",
    17: "En mi entorno de trabajo prima la colaboración sobre la competencia individual.",
    18: "Mi líder directo comunica los objetivos con claridad y sin ambigúedades.",
    19: "Siento que puedo contar con el apoyo técnico de mis superiores ante imprevistos.",
    20: "El clima de mi unidad permite expresar desacuerdos de forma segura.",
    21: "Mi jefatura equilibra las metas con el bienestar del equipo.",
    22: "Recibo información oportuna sobre los cambios que ocurren en la organización.",
    23: "Existe disposición entre compañeros para ayudarnos en momentos de alta carga.",
    24: "Las situaciones de conflicto son gestionadas de forma justa y equitativa.",
    25: "Siento que el esfuerzo que invierto en mi labor es reconocido de forma genuina.",
    26: "Las perspectivas de desarrollo o crecimiento son claras para mí.",
    27: "Percibo que mi salario y beneficios son coherentes con mi responsabilidad.",
    28: "Mi trabajo me entrega una satisfacción personal más allá de lo económico.",
    29: "La organización es justa en la forma en que distribuye premios y méritos.",
    30: "El propósito de mi cargo está alineado con mis valores personales.",
    31: "Me siento valorado como profesional por parte de mi jefatura y pares.",
    32: "Siento que la institución se preocupa por mi estabilidad laboral.",
    33: "Me resulta sencillo desconectarme del trabajo en mis periodos de descanso.",
    34: "Siento que mi entorno personal se ve afectado por la tensión del trabajo.",
    35: "Percibo que debo estar disponible para la organización fuera de mi jornada.",
    36: "Mi vida familiar tiene un espacio respetado por la empresa.",
    37: "Siento que el sistema de trabajo protege mi salud física y mental.",
    38: "He tenido que postergar necesidades personales básicas para cumplir mi labor.",
    39: "La organización fomenta una cultura de desconexión efectiva.",
    40: "Siento que mi nivel de vitalidad es suficiente para los desafíos diarios.",
    41: "¿Sientes que el trabajo te 'persigue' mentalmente después de la salida?",
    42: "¿Has llegado a sentir que nada de lo que hagas cambiará realmente las cosas?",
    43: "¿Prefieres callar tus dificultades para no parecer un eslabón débil?",
    44: "¿Sientes que tu compromiso con la organización se ha enfriado?",
    45: "¿Te sientes tan saturado que te cuesta procesar información nueva?",
    46: "¿Vives con la sensación de que siempre está a punto de ocurrir una emergencia?",
    47: "¿Sientes que el líder de tu área es una fuente de incertidumbre?",
    48: "¿Percibes que la carga administrativa te quita tiempo para lo importante?",
    49: "¿Sientes que el esfuerzo que das es mucho mayor a lo que recibes?",
    50: "¿Te sientes emocionalmente agotado antes de interactuar con colegas?"
}

# --- NAVEGACIÓN ---
if 'paso' not in st.session_state: st.session_state.paso = 'landing'
if 'respuestas' not in st.session_state: st.session_state.respuestas = {}

# --- 1. LANDING PAGE ---
if st.session_state.paso == 'landing':
    st.markdown('<h1 class="landing-title">ASO Master</h1>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1.2, 1], gap="large")
    
    with col_l:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### El Modelo ASO")
        st.write("""
        El Modelo ASO tiene como objetivo detectar los fallos invisibles en el diseño del trabajo que agotan 
        la energía de los equipos. A través de este diagnóstico, obtendrá un mapa de precisión sobre los riesgos 
        neuro-sistémicos de la organización, permitiendo implementar soluciones quirúrgicas que restauran la 
        productividad y protegen la salud mental de los colaboradores.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Instrucciones")
        st.write("Responda con total sinceridad técnica basándose en su realidad operativa actual. La escala va de 1 (Nada de acuerdo) a 5 (Totalmente de acuerdo).")
        if st.button("Comenzar Evaluación", use_container_width=True):
            st.session_state.paso = 'evaluando'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. EVALUACIÓN DINÁMICA ---
elif st.session_state.paso == 'evaluando':
    idx = len(st.session_state.respuestas) + 1
    
    if idx <= 50:
        st.progress(idx / 50)
        
        # Identificar Dimensión
        dim_actual = next(nom for nom, info in dimensiones.items() if idx in info["rango"])
        
        st.markdown(f'<p class="section-label">{dim_actual}</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="question-text">{preguntas_texto[idx]}</p>', unsafe_allow_html=True)
        
        res = st.radio(
            "Seleccione su respuesta:",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: {1:"🔴 Nada de acuerdo", 2:"🟠 En desacuerdo", 3:"🟡 Neutral", 4:"🔵 De acuerdo", 5:"🟢 Totalmente de acuerdo"}[x],
            horizontal=True,
            key=f"radio_{idx}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Confirmar y Continuar", use_container_width=True):
            st.session_state.respuestas[idx] = res
            st.rerun()
    else:
        st.session_state.paso = 'reporte'
        st.rerun()

# --- 3. REPORTE DE ALTA VISIBILIDAD ---
elif st.session_state.paso == 'reporte':
    st.title("📊 Reporte Diagnóstico ASO")
    
    # Procesamiento con Lógica de Inversión[cite: 1]
    promedios = {}
    for nom, info in dimensiones.items():
        vals = [st.session_state.respuestas[i] for i in info["rango"]]
        vals_adj = [6 - v if i in info["inv"] else v for i, v in zip(info["rango"], vals)]
        promedios[nom] = sum(vals_adj) / len(vals_adj)

    df = pd.DataFrame([{"Dimensión": k, "Puntaje": round(v, 2), 
                        "Estado": "RIESGO 🔴" if v >= 3.5 else "ESTABLE 🟢"} 
                       for k, v in promedios.items()])

    c1, c2 = st.columns([1, 1.2], gap="large")
    
    with c1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("### Resumen de Dimensiones")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        fig = px.line_polar(df, r='Puntaje', theta='Dimensión', line_close=True, range_r=[0,5],
                            template="plotly_white")
        fig.update_traces(fill='toself', line_color='#1e3a8a', fillcolor='rgba(30, 58, 138, 0.2)')
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    # Feedback Dual
    eval_col, colab_col = st.columns(2)
    
    with eval_col:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("#### 🔍 Análisis del Evaluador")
        exig = promedios["Exigencias Psicológicas"]
        loop = promedios["Loops Neuropsicológicos"]
        if exig >= 3.5 and loop >= 3.5:
            st.error("Hipótesis: Saturación Sistémica. El colaborador presenta un colapso en la capacidad de recuperación neuro-cognitiva por exceso de demanda.")
        else:
            st.success("Estado: Equilibrio Operativo. No se detectan bloqueos críticos en la infraestructura de trabajo.")
        st.markdown('</div>', unsafe_allow_html=True)

    with colab_col:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("#### 🧠 Estado del Evaluado")
        if promedios["Loops Neuropsicológicos"] >= 3.5:
            st.warning("Tu sistema nervioso está operando en modo alerta constante. Los 'Loops' detectados indican que el trabajo está invadiendo tu capacidad de recuperación mental.")
        else:
            st.success("Tu nivel de vitalidad y capacidad de desconexión se mantienen dentro de márgenes saludables.")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Reiniciar Aplicación"):
        st.session_state.respuestas = {}
        st.session_state.paso = 'landing'
        st.rerun()
