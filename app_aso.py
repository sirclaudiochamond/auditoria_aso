# --- EN LA SECCIÓN DE LANDING PAGE ---
if st.session_state.paso == 'landing':
    st.markdown('<h1 class="landing-title">Auditoría ASO Master</h1>', unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1.5, 1], gap="large")
    
    with col_l:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Identificación Institucional")
        # Nuevo campo para identificar la procedencia
        organizacion = st.text_input("Ingrese el nombre de la Organización / Empresa:", 
                                    placeholder="Ej: Clínica Santa María - Depto. Urgencias")
        
        st.markdown("### ¿Para qué sirve esta evaluación?")
        st.write("Esta herramienta busca entender cómo la organización del trabajo influye en su energía...")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Comienzo")
        if st.button("Iniciar Evaluación", use_container_width=True, type="primary"):
            if organizacion:
                st.session_state.organizacion = organizacion # Guardamos el nombre en la sesión
                st.session_state.paso = 'evaluando'
                st.rerun()
            else:
                st.error("⚠️ Por favor, ingrese el nombre de la organización para continuar.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- EN LA SECCIÓN DE GUARDADO AUTOMÁTICO ---
# Al final, cuando se genera el 'new_row' para Google Sheets:
new_row = pd.DataFrame([{
    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "Organización": st.session_state.organizacion, # Se guarda el nombre capturado al inicio
    "Exigencias": round(promedios["Exigencias Psicológicas"], 2),
    # ... resto de las columnas ...
    "Hipotesis": hipotesis
}])
