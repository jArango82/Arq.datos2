# 🚀 Data Pipeline: Job Salary Prediction Dataset

Un pipeline transforma datos crudos en valor analítico. Este documento describe el flujo ETL (Extracción, Transformación, Carga) diseñado para este proyecto, el cual prepara variables del mercado laboral tecnológico y corporativo para la creación del **Dashboard Interactivo** (`app.py`) y futuros modelos predictivos.

---

## 📥 1. Ingesta (Ingestion)

La primera etapa consiste en la adquisición y recolección de los datos desde su origen hacia nuestro entorno de trabajo.

- **Fuente de Datos:** Dataset extraído originalmente de Kaggle / Fuentes Públicas.
- **Formato Inicial:** Archivo plano CSV (`Data/job_salary_prediction_dataset.csv`).
- **Dimensión Cruda:** 10 columnas que contienen diversas métricas como `job_title`, `experience_years`, `education_level`, `industry`, `remote_work` y nuestro target, `salary`.
- **Estrategia de Extracción:** Carga del archivo a memoria empleando almacenamiento persistente con carga de bajo costo mediante la librería **Pandas**. 

---

## ⚙️ 2. Transformación (Transformation)

Los datos crudos (Raw Data) son procesados para asegurar su integralidad, consistencia y fiabilidad antes del análisis.

- **Limpieza Estructural:**
  - Identificación de tipos de datos de cada columna (Numérica vs. Categórica).
  - Remoción de caracteres especiales o espacios en blanco indeseados en los textos de variables categóricas.

- **Manejo de Valores Nulos y Faltantes (NaN):**
  - **Identificación:** Se evalúa con funciones como `.isnull().sum()`.
  - **Eliminación Segura:** Para las visualizaciones de Streamlit, aplicamos eliminación estricta (`dropna()`) en los features clave de los filtros laterales (`industry`, `remote_work`, `experience_years`).
  - **(Opcional) Imputación:** En el EDA profundo realizado en los Notebooks, se analizaron métodos de imputación para evitar pérdida masiva de datos en columnas no críticas.

- **Normalización y Estandarización:**
  - Conversión estricta a tipos numéricos o de texto consistentes. Ej: asegurar que las listas de elementos únicos (Unique Lists) sean convertidos a tipo *String* (`[str(i) for i in industries]`) para prevenir fallos (panics) en los bundles JavaScript de módulos en producción.
  - Ordenamiento alfabético (`sorted()`) para menús desplegables consistentes.

---

## 📤 3. Carga (Load)

La última etapa del pipeline, donde los datos refinados están listos para entregar valor al usuario final.

- **Estructura Final:** Un DataFrame de Pandas completamente estructurado (Golden Dataset o Data Warehouse / Data Mart en miniatura).
- **Consumo (Delivery):** La aplicación construida en Streamlit usa estos datos en memoria como única fuente de verdad (Single Source of Truth).
- **Optimización de Consultas:** Se aplica la directiva `@st.cache_data` para guardar en caché los resultados tras ejecutarse el flujo de lectura y transformación por primera vez. Esto previene un gasto excesivo en coste computacional ante múltiples interacciones de los filtros en tiempo real. 

---

> *"De 0s y 1s a Decisiones de Negocio."*
