import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE MARCA Y ESTILO ---
st.set_page_config(page_title="ASO Master - Auditoría Neuro-Sistémica", layout="wide")

# Inyección de CSS para legibilidad y dinamismo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main { background-color: #fcfcfd; }
    .stProgress > div > div > div > div { background-color: #3b82f6; }
    
    /* Card de pregunta */
    .question-card {
        background-color: white;
        padding: 40px;
        border-radius: 24px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .instruction-text { color: #6b7280; font-size: 1.1rem; }
    .header-title { color: #1e3a8a; font-weight: 800; font-size: 2.8rem; margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE CONOCIMIENTO (50 ÍTEMS) ---
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

# --- ESTADO DE NAVEGACIÓN ---
if 'paso' not in st.session_state: st.session_state.paso = 'landing'
if 'respuestas' not in st.session_state: st.session_state.respuestas = {}

# --- 1. LANDING PAGE ---
if st.session_state.paso == 'landing':
    st.markdown('<h1 class="header-title">Proyecto ASO Master</h1>', unsafe_allow_html=True)
    st.markdown('### Auditoría de Salud Organizacional (Versión 2026)')
    
    col_l, col_r = st.columns([1, 1], gap="large")
    
    with col_l:
        st.info("**Propósito Metodológico**")
        st.write("""
        Esta auditoría no es una encuesta de clima tradicional. Es un escáner de precisión que utiliza 
        **neurobiología aplicada** para detectar fallos sistémicos en el entorno de trabajo.[cite: 1, 2]
        
        Evaluamos 50 puntos críticos que determinan si su equipo está operando en 
        **Eficiencia Cognitiva** o en **Modo Supervivencia**.
        """)
        
        st.success("**Instrucciones de Respuesta**")
        st.write("""
        1. **Sinceridad técnica**: Responda según su realidad operativa diaria.
        2. **Escala**: 1 es 'Totalmente en desacuerdo' y 5 es 'Totalmente de acuerdo'.
        3. **Tiempo**: El proceso toma aproximadamente 8-10 minutos.
        """)

    with col_r:
        st.markdown("### El Modelo ASO")
        st.markdown("""
        - **6 Dimensiones Críticas**: Desde carga mental hasta loops de agotamiento.
        - **Punto de Corte de Riesgo**: $\\bar{X} \\geq 3.5$.[cite: 1]
        - **Metodología 60/40**: El diagnóstico define el foco de la capacitación.[cite: 2]
        """)
        if st.button("Iniciar Evaluación Ahora", use_container_width=True, type="primary"):
            st.session_state.paso = 'evaluando'
            st.rerun()

# --- 2. CUESTIONARIO DINÁMICO ---
elif st.session_state.paso == 'evaluando':
    idx = len(st.session_state.respuestas) + 1
    
    if idx <= 50:
        # Barra de progreso dinámica
        st.progress(idx / 50)
        
        # Identificar Dimensión
        dim_actual = next(nom for nom, info in dimensiones.items() if idx in info["rango"])
        
        st.markdown(f"**Dimensión actual:** {dim_actual}")
        
        # Card de Pregunta
        with st.container():
            st.markdown(f"""<div class="question-card">
                <p class="instruction-text">Pregunta {idx} de 50</p>
                <h2 style="font-size: 1.8rem; margin-bottom: 2rem;">{preguntas_texto[idx]}</h2>
                </div>""", unsafe_allow_html=True)
            
            res = st.select_slider(
                "Mueva el control hacia su nivel de acuerdo:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1:"Totalmente en desacuerdo", 2:"En desacuerdo", 3:"Neutral", 4:"De acuerdo", 5:"Totalmente de acuerdo"}[x],
                key=f"slider_{idx}"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Confirmar y Siguiente", use_container_width=True):
                st.session_state.respuestas[idx] = res
                st.rerun()
    else:
        st.session_state.paso = 'reporte'
        st.rerun()

# --- 3. REPORTE DIAGNÓSTICO PROFUNDO ---
elif st.session_state.paso == 'reporte':
    st.header("📊 Resultado del Diagnóstico de Salud Organizacional")
    
    # Lógica de Inversión $S_{final} = 6 - S_{raw}$[cite: 1, 2]
    promedios = {}
    for nom, info in dimensiones.items():
        vals = [st.session_state.respuestas[i] for i in info["rango"]]
        vals_adj = [6 - v if i in info["inv"] else v for i, v in zip(info["rango"], vals)]
        promedios[nom] = sum(vals_adj) / len(vals_adj)

    df = pd.DataFrame([{"Dimensión": k, "Puntaje": round(v, 2), 
                        "Estado": "RIESGO 🔴" if v >= 3.5 else "ESTABLE 🟢"} 
                       for k, v in promedios.items()])

    # Visualización SaaS
    col_chart, col_data = st.columns([1.5, 1])
    with col_chart:
        fig = px.line_polar(df, r='Puntaje', theta='Dimensión', line_close=True, range_r=[0,5],
                            template="plotly_white", title="Ecosistema de Riesgo Sistémico")
        fig.update_traces(fill='toself', line_color='#1e3a8a')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_data:
        st.write("### Resumen Técnico")
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # BLOQUE DE DIAGNÓSTICO PROFUNDO[cite: 1, 2]
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 🧠 Para el Colaborador")
        with st.container():
            p_loops = promedios["Loops Neuropsicológicos"]
            if p_loops >= 3.5:
                st.warning(f"**Alerta de Saturación ({p_loops}):** Su sistema nervioso indica dificultad para 'cerrar' el ciclo laboral. Esto suele manifestarse como rumiación mental y fatiga al despertar.")
            else:
                st.success("Su sistema de recuperación neuro-cognitiva se mantiene funcional.")
            
            p_vida = promedios["Vida Personal"]
            if p_vida >= 3.5:
                st.error(f"**Interferencia Crítica ({p_vida}):** Existe un desborde del trabajo hacia su espacio vital. Es urgente aplicar protocolos de desconexión efectiva.")

    with c2:
        st.markdown("#### 🔍 Para el Evaluador (Claudio Chamond)")
        exig = promedios["Exigencias Psicológicas"]
        ctrl = promedios["Control y Autonomía"]
        
        # Hipótesis basada en Job Strain[cite: 1]
        if exig >= 3.5 and ctrl >= 3.5:
            st.error("**Hipótesis: Job Strain Extremo.** Combinación de alta demanda y bajo control. Riesgo inminente de burnout e incremento de licencias médicas.")
        elif exig >= 3.5 and ctrl < 3.5:
            st.warning("**Hipótesis: Saturación Sistémica.** El volumen de tareas ha colapsado la autonomía. Se requiere intervención estructural en procesos.")
        else:
            st.success("**Estado: Equilibrio Dinámico.** El sistema de trabajo es demandante pero sostenible.")

    if st.button("Reiniciar Auditoría"):
        st.session_state.respuestas = {}
        st.session_state.paso = 'landing'
        st.rerun()
