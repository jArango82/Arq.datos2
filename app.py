import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración básica de página
st.set_page_config(
    page_title="Salary Analytics",
    page_icon="📊",
    layout="wide"
)

# Título Principal
st.title("📊 Dashboard de Salarios Tech")
st.markdown("Análisis interactivo de salarios basado en el dataset proporcionado.")

# Carga de datos robusta
@st.cache_data
def load_data():
    paths_to_try = [
        "Data/job_salary_prediction_dataset.csv",
        "job_salary_prediction_dataset.csv" 
    ]
    for path in paths_to_try:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

df = load_data()

if df is not None:
    # --- SIDEBAR ---
    st.sidebar.header("🎯 Filtros")
    
    # Filtro Industry
    industries = sorted(df['industry'].unique().tolist())
    selected_ind = st.sidebar.multiselect("Sector:", industries, default=industries[:2])

    # Filtro Experience
    min_e, max_e = int(df['experience_years'].min()), int(df['experience_years'].max())
    experience = st.sidebar.slider("Años Experiencia:", min_e, max_e, (min_e, max_e))

    # Filtrado
    mask = (df['experience_years'].between(experience[0], experience[1]))
    if selected_ind:
        mask &= (df['industry'].isin(selected_ind))
    
    filtered_df = df[mask]

    # --- MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Registros", f"{len(filtered_df):,}")
    m2.metric("Salario Promedio", f"${filtered_df['salary'].mean():,.0f}")
    m3.metric("Exp. Promedio", f"{filtered_df['experience_years'].mean():.1f} años")

    st.divider()

    # --- VISUALIZACIONES ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución Salarial")
        fig1 = px.histogram(filtered_df, x="salary", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Experiencia vs Salario")
        fig2 = px.scatter(filtered_df, x="experience_years", y="salary", 
                         color="education_level", opacity=0.6)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Salario por Industria")
        avg_ind = filtered_df.groupby('industry')['salary'].mean().sort_values()
        fig3 = px.bar(avg_ind, orientation='h')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Ubicaciones Principales")
        locs = filtered_df['location'].value_counts().head(10)
        fig4 = px.pie(values=locs.values, names=locs.index, hole=0.3)
        st.plotly_chart(fig4, use_container_width=True)

else:
    st.error("No se pudo cargar el archivo CSV. Verifica que esté en la carpeta 'Data/'.")
