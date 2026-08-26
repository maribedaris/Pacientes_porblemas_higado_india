"""Demo interactiva del modelo GaussianNB entrenado para detección de problemas
de hígado. Ejecutar con: streamlit run notebooks/7-deploy/streamlit_app.py"""

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_MODELO = RAIZ_PROYECTO / "models" / "pacientes_higado_clasificacion-gaussiannb-v2.joblib"
RUTA_METADATOS = RAIZ_PROYECTO / "models" / "pacientes_higado_clasificacion-gaussiannb-v2.json"


@st.cache_resource
def cargar_modelo() -> tuple[object, float]:
    """Carga el pipeline y el umbral de decisión; el umbral NO está en el joblib."""
    modelo = joblib.load(RUTA_MODELO)
    metadatos = json.loads(RUTA_METADATOS.read_text(encoding="utf-8"))
    return modelo, float(metadatos["umbral_decision"])


st.set_page_config(
    page_title="Demo — Detección de problemas de hígado", page_icon="🩺", layout="centered"
)

st.title("🩺 Detección de problemas de hígado")
st.caption(
    "Demo del modelo GaussianNB entrenado en el proyecto de pacientes de India (etapa de modelos, 2026)."
)

st.warning(
    "**Aviso:** esta demo es un proyecto educativo. No es un dispositivo médico, "
    "no tiene validación clínica y no sustituye la evaluación de un profesional de la salud.",
    icon="⚠️",
)

modelo, umbral = cargar_modelo()

st.divider()
st.subheader("Datos del paciente")
col_izq, col_der = st.columns(2)

with col_izq:
    edad = st.number_input("Edad (años)", min_value=1, max_value=110, value=45, step=1)
    bilirrubina_total = st.number_input(
        "Bilirrubina total (mg/dL)", min_value=0.0, max_value=80.0, value=1.0, step=0.1
    )
    bilirrubina_directa = st.number_input(
        "Bilirrubina directa (mg/dL)", min_value=0.0, max_value=25.0, value=0.3, step=0.1
    )
    fosfatasa = st.number_input(
        "Fosfatasa alcalina (U/L)", min_value=0, max_value=2200, value=208, step=1
    )
    genero = st.selectbox("Género", ["Male", "Female"])

with col_der:
    alt = st.number_input(
        "ALT — alanina aminotransferasa (U/L)", min_value=0, max_value=2100, value=35, step=1
    )
    ast = st.number_input(
        "AST — aspartato aminotransferasa (U/L)", min_value=0, max_value=5000, value=41, step=1
    )
    proteinas = st.number_input(
        "Proteínas totales (g/dL)", min_value=0.0, max_value=12.0, value=6.6, step=0.1
    )
    albumina = st.number_input("Albúmina (g/dL)", min_value=0.0, max_value=7.0, value=3.1, step=0.1)
    ratio_ag = st.number_input(
        "Ratio albúmina/globulina", min_value=0.0, max_value=4.0, value=0.95, step=0.01
    )

if bilirrubina_directa > bilirrubina_total:
    st.error(
        "La bilirrubina directa no puede superar a la bilirrubina total (restricción fisiológica)."
    )
    st.stop()

paciente = pd.DataFrame(
    {
        "Age": [edad],
        "Gender": [genero],
        "Total_Bilirubin": [bilirrubina_total],
        "Direct_Bilirubin": [bilirrubina_directa],
        "Alkaline_Phosphotase": [fosfatasa],
        "Alamine_Aminotransferase": [alt],
        "Aspartate_Aminotransferase": [ast],
        "Total_Protiens": [proteinas],
        "Albumin": [albumina],
        "Albumin_and_Globulin_Ratio": [ratio_ag],
    }
)

st.divider()
if st.button("Predecir", type="primary", use_container_width=True):
    # el umbral viaja en el JSON, no en el pipeline: NUNCA usar modelo.predict()
    probabilidad = float(modelo.predict_proba(paciente)[:, 1][0])
    clasificacion = int(probabilidad >= umbral)

    if clasificacion == 1:
        st.error(
            f"**Clasificación: posibles problemas de hígado** (score {probabilidad:.3f})", icon="🔴"
        )
    else:
        st.success(
            f"**Clasificación: sin indicios de problemas** (score {probabilidad:.3f})", icon="🟢"
        )

    st.markdown(
        f"El score crudo del modelo es **{probabilidad:.3f}**, comparado contra el umbral de decisión "
        f"**{umbral:.4f}** calibrado en la etapa de selección. Este score **no es un porcentaje de riesgo "
        "calibrado**: el modelo asume independencia entre variables que en realidad están correlacionadas "
        "(como las dos bilirrubinas), lo que infla su confianza numérica. Úselo como ordenamiento "
        "(más alto = más indicios), no como probabilidad clínica."
    )

st.divider()
with st.expander("📊 Limitaciones y métricas del modelo (transparencia)"):
    st.markdown(
        """**Métricas reales en el conjunto de prueba (114 pacientes no vistos en entrenamiento):**

| Métrica | Valor |
|---|---|
| f1_macro | 0.741 |
| roc_auc | 0.861 |
| Recall clase "sin problemas" (especificidad) | 81.8 % |
| Recall clase "problemas de hígado" (sensibilidad) | 74.1 % |

Es decir: aproximadamente 1 de cada 4 pacientes enfermos no sería detectado, y cerca de
1 de cada 5 pacientes sanos recibiría una alarma innecesaria.

**Sobre los datos de entrenamiento:** el modelo se entrenó con 566 pacientes de un
dataset público de India. Es un conjunto pequeño y geográficamente acotado; valores de
laboratorio muy fuera de los rangos típicos de ese dataset pueden producir resultados
poco fiables."""
    )
