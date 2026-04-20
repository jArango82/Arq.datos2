import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración de página
st.set_page_config(
    page_title="Salary Analytics Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para que luzca muy atractivo
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stApp {
        background-image: radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                          radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
        background-attachment: fixed;
    }
    .metric-card {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 {
        color: #e2e8f0;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Cacheamos la carga de datos para mejor rendimiento
@st.cache_data
def load_data():
    file_path = "Data/job_salary_prediction_dataset.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        # Fallback en caso de ejecutar app.py desde otra ruta
        st.error(f"No se encontró el dataset en {file_path}")
        df = pd.DataFrame()
    return df

df = load_data()

if not df.empty:
    st.title("💼 Dashboard Interactivo de Salarios Tech")
    st.markdown("Análisis descriptivo y exploración dinámica del mercado laboral.")

    # SIDEBAR - Filtros Dinámicos
    st.sidebar.header("🎯 Filtros Dinámicos")
    
    df = df.dropna(subset=['industry', 'remote_work', 'experience_years'])

    # Filtro Industry (selectbox en lugar de multiselect)
    industries = sorted([str(i) for i in df['industry'].unique() if pd.notna(i)])
    industry_options = ["Todas"] + industries
    selected_industry = st.sidebar.selectbox("Sector Industrial", industry_options, index=0)

    # Filtro Remote Work (radio en lugar de multiselect)
    remote_raw = sorted([str(r) for r in df['remote_work'].unique() if pd.notna(r)])
    remote_options = ["Todas"] + remote_raw
    selected_remote = st.sidebar.radio("Modalidad de Trabajo", remote_options, index=0)

    # Filtro Experience Years (number_input en lugar de slider)
    min_exp = int(df['experience_years'].min())
    max_exp = int(df['experience_years'].max())
    exp_min = st.sidebar.number_input("Experiencia mínima (años)", min_value=min_exp, max_value=max_exp, value=min_exp)
    exp_max = st.sidebar.number_input("Experiencia máxima (años)", min_value=min_exp, max_value=max_exp, value=max_exp)

    # APLICAR FILTROS
    mask = (df['experience_years'] >= exp_min) & (df['experience_years'] <= exp_max)
    if selected_industry != "Todas":
        mask &= (df['industry'] == selected_industry)
    if selected_remote != "Todas":
        mask &= (df['remote_work'] == selected_remote)
    filtered_df = df[mask]

    # KPIS PRINCIPALES
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Registros Analizados</div><div class="metric-value">{len(filtered_df):,}</div></div>', unsafe_allow_html=True)
    with col2:
        avg_salary = filtered_df['salary'].mean()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Salario Promedio</div><div class="metric-value">${avg_salary:,.0f}</div></div>', unsafe_allow_html=True)
    with col3:
        max_salary = filtered_df['salary'].max()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Salario Máximo</div><div class="metric-value">${max_salary:,.0f}</div></div>', unsafe_allow_html=True)
    with col4:
        avg_exp = filtered_df['experience_years'].mean()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Experiencia Promedio</div><div class="metric-value">{avg_exp:.1f} años</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # FILA 1 DE GRAFICOS
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Distribución Salarial")
        fig_hist = px.histogram(
            filtered_df, x="salary", nbins=50, 
            color_discrete_sequence=["#3b82f6"],
            template="plotly_dark"
        )
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        st.subheader("📈 Salario vs Años de Experiencia")
        # Mostramos una muestra para graficos scatter si hay muchos datos para no saturar al usuario
        sample_df = filtered_df.sample(min(2000, len(filtered_df))) if len(filtered_df) > 2000 else filtered_df
        fig_scatter = px.scatter(
            sample_df, x="experience_years", y="salary", 
            color="education_level", 
            template="plotly_dark",
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)

    # FILA 2 DE GRAFICOS
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("🏢 Promedio Salarial por Industria")
        industry_salary = filtered_df.groupby('industry')['salary'].mean().reset_index().sort_values('salary', ascending=True)
        fig_bar = px.bar(
            industry_salary, x="salary", y="industry", orientation='h',
            color="salary", color_continuous_scale="Purp",
            template="plotly_dark"
        )
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c4:
        st.subheader("🏠 Modalidad de Trabajo")
        remote_counts = filtered_df['remote_work'].value_counts().reset_index()
        remote_counts.columns = ['remote_work', 'count']
        fig_pie = px.pie(
            remote_counts, names='remote_work', values='count', 
            hole=0.4, # Donut chart
            color_discrete_sequence=["#10b981", "#3b82f6", "#8b5cf6"],
            template="plotly_dark"
        )
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    # FILA 3 (MÁS GRAFICOS)
    c5, c6 = st.columns(2)
    
    with c5:
        st.subheader("📦 Distribución Salarial por Tamaño de Empresa")
        fig_box = px.box(
            filtered_df, x="company_size", y="salary", 
            color="company_size",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_box.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_box, use_container_width=True)

    with c6:
        st.subheader("🌍 Top 10 Ubicaciones por Volúmen")
        loc_counts = filtered_df['location'].value_counts().head(10).reset_index()
        loc_counts.columns = ['location', 'count']
        fig_loc = px.bar(
            loc_counts, x="location", y="count",
            color="count", color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig_loc.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_loc, use_container_width=True)

else:
    st.warning("⚠️ No se pudieron cargar los datos o el dataset está vacío.")
