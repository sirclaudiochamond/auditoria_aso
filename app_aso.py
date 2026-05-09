import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN TÉCNICA Y ESTÉTICA ---
st.set_page_config(page_title="ASO Master - Auditoría de Salud", layout="wide")

# CSS Optimizado para "Zero-Scroll" en fase de cuestionario
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    /* Eliminar paddings de Streamlit para ganar espacio vertical */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    footer {visibility: hidden;}
    header {visibility: hidden;}

    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #fcfcfd; }
    
    /* Card de Pregunta Compacta */
    .main-card {
        background-color: white;
        padding: 25px 35px;
        border-radius: 24px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
        margin-bottom: 10px;
    }
    
    .question-number { color: #3b82f6; font-weight: 800; font-size: 1rem; margin-bottom: 2px; }
    .question-text { 
        font-size: 1.9rem; /* Ajustado para caber sin scroll */
        font-weight: 700; 
        color: #0f172a; 
        line-height: 1.1; 
        margin-bottom: 20px; 
    }

    /* Alternativas Verticales Compactas */
    div.stRadio > div { flex-direction: column !important; gap: 8px; }
    
    label[data-baseweb="radio"] {
        background-color: #ffffff;
        padding: 12px 20px !important; /* Más delgado para ahorrar espacio */
        border-radius: 14px !important;
        border: 2px solid #f1f5f9 !important;
        width: 100%;
        transition: all 0.2s ease;
    }

    label[data-baseweb="radio"]:hover { border-color: #3b82f6 !important; background-color: #f0f7ff !important; }
    div[data-testid="stMarkdownContainer"] p { font-size: 1.1rem !important; font-weight: 600; }
    
    .landing-title { font-size: 3rem; font-weight: 800; color: #1e3a8a; letter-spacing: -0.04em; }
    </style>
    """, unsafe_allow_html=True)

# --- DEFINICIONES Y METADATOS ---
# Basado en la metodología de Auditoría de Salud Organizacional
definiciones = {
    "Exigencias Psicológicas": "Mide la presión de tiempo, la velocidad requerida y el volumen de tareas que deben procesarse simultáneamente.",
    "Control y Autonomía": "Evalúa el margen de decisión que tiene sobre su agenda y la posibilidad de aplicar sus conocimientos en su puesto.",
    "Apoyo Social y Liderazgo": "Analiza la calidad de la relación con superiores y compañeros, y el respaldo técnico que recibe ante problemas.",
    "Recompensa y Sentido": "Refleja el reconocimiento recibido y si siente que su labor tiene un propósito alineado con sus valores.",
    "Vida Personal": "Identifica si el trabajo interfiere con sus periodos de descanso o si permite una desconexión mental efectiva.",
    "Loops Neuropsicológicos": "Detecta círculos viciosos de cansancio mental donde el esfuerzo no genera resultados, provocando saturación cognitiva."
}

dimensiones = {
    "Exigencias Psicológicas": {"rango": range(1, 9), "inv": []},
    "Control y Autonomía": {"rango": range(9, 17), "inv": range(9, 17)},
    "Apoyo Social y Liderazgo": {"rango": range(17, 25), "inv": range(17, 25)},
    "Recompensa y Sentido": {"rango": range(25, 33), "inv": range(25, 33)},
    "Vida Personal": {"rango": range(33, 41), "inv": [33, 36, 37, 39, 40]},
    "Loops Neuropsicológicos": {"rango": range(41, 51), "inv": []}
}

# Texto íntegro de las 50 preguntas
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

# --- ESTADO DE SESIÓN ---
if 'paso' not in st.session_state: st.session_state.paso = 'landing'
if 'respuestas' not in st.session_state: st.session_state.respuestas = {}

# --- 1. LANDING PAGE ---
if st.session_state.paso == 'landing':
    st.markdown('<h1 class="landing-title">Auditoría ASO Master</h1>', unsafe_allow_html=True)
    col_l, col_r = st.columns([1.5, 1], gap="medium")
    with col_l:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### ¿Para qué sirve esta evaluación?")
        st.write("""
        Esta herramienta busca entender cómo la forma en que está organizado su trabajo diario influye en su energía y bienestar. 
        El objetivo no es evaluarlo a usted personalmente, sino identificar bloqueos en el diseño del sistema que puedan estar 
        generando cansancio excesivo o dificultando su labor. Al responder, nos ayuda a proponer mejoras concretas que faciliten 
        su día a día, restauren la productividad y protejan su salud mental.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_r:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Instrucciones")
        st.write("- Elija la opción que mejor refleje su realidad operativa actual.")
        st.write("- Sea sincero: sus respuestas son la base para proponer cambios reales.")
        if st.button("Comenzar Evaluación", use_container_width=True, type="primary"):
            st.session_state.paso = 'evaluando'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CUESTIONARIO COMPACTO (ZERO-SCROLL) ---
elif st.session_state.paso == 'evaluando':
    idx = len(st.session_state.respuestas) + 1
    if idx <= 50:
        st.progress(idx / 50)
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="question-number">Pregunta {idx} de 50</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="question-text">{preguntas_texto[idx]}</p>', unsafe_allow_html=True)
        
        res = st.radio(
            "Su nivel de acuerdo:",
            options=[5, 4, 3, 2, 1],
            format_func=lambda x: {5:"Totalmente de acuerdo", 4:"De acuerdo", 3:"Neutral", 2:"En desacuerdo", 1:"Totalmente en desacuerdo"}[x],
            key=f"radio_{idx}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Siguiente", use_container_width=True):
            st.session_state.respuestas[idx] = res
            st.rerun()
    else:
        st.session_state.paso = 'reporte'
        st.rerun()

# --- 3. REPORTE INTEGRAL ---
elif st.session_state.paso == 'reporte':
    st.header("📊 Informe Integral de Salud Organizacional")
    
    # Lógica de Inversión basada en la Metodología ASO Master
    promedios = {}
    for nom, info in dimensiones.items():
        vals = [st.session_state.respuestas[i] for i in info["rango"]]
        vals_adj = [6 - v if i in info["inv"] else v for i, v in zip(info["rango"], vals)]
        promedios[nom] = sum(vals_adj) / len(vals_adj)

    df = pd.DataFrame([{"Dimensión": k, "Definición": definiciones[k], "Puntaje": round(v, 2), 
                        "Estado": "RIESGO 🔴" if v >= 3.5 else "ESTABLE 🟢"} 
                       for k, v in promedios.items()])

    col_chart, col_info = st.columns([1.2, 1])
    with col_chart:
        fig = px.line_polar(df, r='Puntaje', theta='Dimensión', line_close=True, range_r=[0,5],
                            template="plotly_white", title="Ecosistema Sistémico")
        fig.update_traces(fill='toself', line_color='#1e3a8a', fillcolor='rgba(30, 58, 138, 0.2)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("### Resumen de Estado")
        st.dataframe(df[["Dimensión", "Puntaje", "Estado"]], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("## Análisis Detallado de Resultados")
    st.write("Este informe integra la visión técnica y personal para comprender la dinámica de trabajo actual.")

    for index, row in df.iterrows():
        with st.expander(f"{row['Dimensión']} ({row['Estado']})", expanded=True):
            st.write(f"**¿Qué evalúa?:** {row['Definición']}")
            puntaje = row['Puntaje']
            if puntaje >= 3.5:
                st.error(f"Puntaje: {puntaje}. Se observa un desequilibrio que puede estar afectando el rendimiento y la vitalidad.")
            else:
                st.success(f"Puntaje: {puntaje}. Esta área se encuentra en equilibrio dinámico.")

    st.divider()
    
    # Hipótesis y Plan de Acción basados en Metodología ASO
    st.write("### Conclusión y Hoja de Ruta")
    exig = promedios["Exigencias Psicológicas"]
    loop = promedios["Loops Neuropsicológicos"]
    
    if exig >= 3.5 and loop >= 3.5:
        st.error("**Situación Detectada: Saturación Sistémica.** El volumen de tareas ha sobrepasado la capacidad de recuperación natural. Esto genera 'Loops' de cansancio donde la sensación de avance disminuye.")
    elif exig >= 3.5:
        st.warning("**Situación Detectada: Sobrecarga Operativa.** La demanda es alta, pero el sistema aún no colapsa. Es el momento preventivo ideal.")
    else:
        st.success("**Situación Detectada: Estabilidad Operativa.** El diseño de tareas es coherente con la capacidad instalada del equipo.")

    st.write("#### Próximos Pasos Sugeridos:")
    st.write("1. **Revisión de Procesos:** Analizar la distribución de tareas en las áreas marcadas en rojo.")
    st.write("2. **Protocolos de Desconexión:** Fortalecer la barrera entre el trabajo y la vida personal para desactivar loops de rumiación.")
    st.write("3. **Capacitación Focalizada:** Entrenar en herramientas específicas de gestión neuro-cognitiva basadas en estos resultados.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Reiniciar Sistema"):
        st.session_state.respuestas = {}
        st.session_state.paso = 'landing'
        st.rerun()
