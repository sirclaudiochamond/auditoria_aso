import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de Rigidez Metodológica ASO 2026
st.set_page_config(page_title="ASO Master - Diagnóstico Profundo", layout="wide")

# --- LÓGICA DE DATOS Y DIMENSIONES ---
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

# --- ESTADO DE SESIÓN ---
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}
if 'paso' not in st.session_state:
    st.session_state.paso = 'inicio'

# --- INTERFAZ ---
if st.session_state.paso == 'inicio':
    st.title("🛡️ Auditoría ASO: Diagnóstico Profundo")
    st.write("Bienvenido al sistema de evaluación neuro-sistémica Claudio Chamond. Este diagnóstico evalúa la infraestructura de su salud organizacional.")
    if st.button("Iniciar Evaluación"):
        st.session_state.paso = 'evaluando'
        st.rerun()

elif st.session_state.paso == 'evaluando':
    idx = len(st.session_state.respuestas) + 1
    if idx <= 50:
        st.progress(idx / 50)
        st.subheader(preguntas_texto[idx])
        res = st.radio("Respuesta:", [5, 4, 3, 2, 1], 
                       format_func=lambda x: {5:"Totalmente de acuerdo", 4:"De acuerdo", 3:"Neutral", 2:"En desacuerdo", 1:"Totalmente en desacuerdo"}[x],
                       horizontal=True, key=f"p{idx}")
        if st.button("Siguiente"):
            st.session_state.respuestas[idx] = res
            st.rerun()
    else:
        st.session_state.paso = 'reporte'
        st.rerun()

elif st.session_state.paso == 'reporte':
    st.header("📊 Reporte de Salud Organizacional (Perfil 360°)")
    
    # Procesamiento con Lógica de Inversión[cite: 1]
    resultados = []
    dict_promedios = {}
    for nom, info in dimensiones.items():
        vals = [st.session_state.respuestas[i] for i in info["rango"]]
        vals_adj = [6 - v if i in info["inv"] else v for i, v in zip(info["rango"], vals)]
        prom = sum(vals_adj) / len(vals_adj)
        dict_promedios[nom] = prom
        estado = "CRÍTICO 🔴" if prom >= 3.5 else "ESTABLE 🟢" # Punto de corte 3.5[cite: 1]
        resultados.append({"Dimensión": nom, "Puntaje": round(prom, 2), "Estado": estado})

    df = pd.DataFrame(resultados)
    
    # --- VISUALIZACIÓN ---
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.table(df)
    with col2:
        fig = px.line_polar(df, r='Puntaje', theta='Dimensión', line_close=True, range_r=[0,5], title="Ecosistema Sistémico")
        st.plotly_chart(fig)

    st.divider()

    # --- SECCIÓN: PARA EL COLABORADOR (Feedback Empático/Neuro) ---
    st.subheader("💡 Mi Estado: Autoconocimiento")
    exp_col = st.expander("Haz clic para comprender tu situación actual", expanded=True)
    with exp_col:
        if dict_promedios["Loops Neuropsicológicos"] >= 3.5:
            st.warning("**Saturación de Señal:** Tu cerebro está operando en 'modo emergencia'. La sensación de que el trabajo no termina al salir indica que tu sistema de recuperación está bloqueado por la alta demanda.")
        if dict_promedios["Exigencias Psicológicas"] >= 3.5:
            st.write("- **Carga Cognitiva:** Estás procesando un volumen de información que supera el umbral de eficiencia, lo que genera fatiga prefrontal.")
        if dict_promedios["Control y Autonomía"] < 3.5:
            st.write("- **Autonomía:** Posees margen de decisión, lo cual es un factor protector, aunque la carga actual dificulta su ejercicio.")
        else:
            st.error("- **Rigidez en el Rol:** Te sientes atrapado en procedimientos que no puedes modificar, aumentando la sensación de indefensión.")

    # --- SECCIÓN: PARA EL EVALUADOR (Análisis Clínico/Metodológico) ---
    st.subheader("🔍 Análisis para el Evaluador (Claudio Chamond)")
    exp_eval = st.expander("Variables Técnicas e Hipótesis Diagnóstica", expanded=True)
    with exp_eval:
        # Cruce de Variables para Hipótesis
        exig = dict_promedios["Exigencias Psicológicas"]
        loop = dict_promedios["Loops Neuropsicológicos"]
        ctrl = dict_promedios["Control y Autonomía"]
        
        st.write("### Hipótesis Diagnóstica:")
        if exig >= 3.5 and loop >= 3.5 and ctrl < 3.5:
            st.error("**Saturación Sistémica por Carga Excesiva:** El colaborador presenta una alta demanda con alta autonomía, pero el volumen ha colapsado la función ejecutiva, activando Loops de rumiación. No es un problema de competencias, es un problema de caudal de tareas.")
        elif exig >= 3.5 and ctrl >= 3.5:
            st.error("**Tensión Laboral (Job Strain):** Escenario de alto riesgo. La combinación de alta demanda y bajo control es el predictor número uno de patología por estrés crónico.")
        else:
            st.success("**Sistema en Equilibrio Dinámico:** No se observan bloqueos neuro-sistémicos significativos.")

        st.write("### Plan de Intervención (Metodología 60/40):")
        st.write(f"- **60% Estructural:** Sesiones de recuperación neuro-cognitiva para desactivar Loops (ACT/Mindfulness).")
        st.write(f"- **40% Focalizado:** Intervención en los procesos de la dimensión: **{df.loc[df['Puntaje'].idxmax(), 'Dimensión']}**.")

    if st.button("Reiniciar Evaluación"):
        st.session_state.respuestas = {}
        st.session_state.paso = 'inicio'
        st.rerun()
