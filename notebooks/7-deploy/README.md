# Demo interactiva del modelo (Streamlit)

Esta demo permite probar en el navegador el modelo GaussianNB seleccionado como el
mejor del proyecto (f1_macro 0.741, roc_auc 0.861 en el conjunto de prueba): se
ingresan los valores de laboratorio de un paciente y la app devuelve la clasificación
con el umbral calibrado (0.0011), junto con las advertencias correspondientes.

## Cómo correr la demo localmente

Requisitos: Python 3.12 y un gestor de entornos (el proyecto usa `uv`, pero `pip`
también sirve).

**Opción A — desde la raíz del repositorio** (recomendada, deja el proyecto completo
a mano):

```bash
python -m venv .venv-demo
source .venv-demo/bin/activate      # en Windows: .venv-demo\Scripts\activate
pip install -r notebooks/7-deploy/requirements.txt
streamlit run notebooks/7-deploy/streamlit_app.py
```

**Opción B — parado dentro de `notebooks/7-deploy/`**:

```bash
cd notebooks/7-deploy
python -m venv .venv-demo
source .venv-demo/bin/activate      # en Windows: .venv-demo\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

En ambos casos la app localiza sola la raíz del proyecto (vía la ubicación de su
propio archivo) y carga el modelo desde
`models/pacientes_higado_clasificacion-gaussiannb-v2.joblib`, así que debe ejecutarse
desde un checkout completo del repositorio, no de la carpeta suelta.

## Demo desplegada

- [Link de la demo desplegada — agregar tras conectar el repo a Streamlit Cloud]
- [Screenshot — agregar tras probar la demo desplegada]

## Cómo desplegar en Streamlit Community Cloud (manual, una sola vez)

El despliegue requiere iniciar sesión con la cuenta de GitHub del dueño del repo, por
lo que se hace manualmente:

1. Verificar que el repositorio es **público** en GitHub (requisito del plan gratuito
   de Streamlit Cloud).
2. Entrar a [share.streamlit.io](https://share.streamlit.io) e iniciar sesión con la
   cuenta de GitHub.
3. Pulsar **New app**.
4. En el formulario: seleccionar el repositorio (`Pacientes_porblemas_higado_india`),
   la rama (`main`) y como **main file path** indicar `notebooks/7-deploy/streamlit_app.py`
   — la app vive en esa subcarpeta, no en la raíz, así que hay que especificarlo.
5. Pulsar **Deploy** y esperar unos minutos a que instale
   `notebooks/7-deploy/requirements.txt`.
6. Una vez desplegada, copiar el enlace y reemplazar el placeholder de arriba; probar
   la demo y agregar el screenshot.

## Detalles técnicos relevantes

- **El umbral no viaja dentro del joblib**: el pipeline expone `predict_proba`, y la
  clasificación correcta es `(predict_proba(X)[:, 1] >= 0.0011)`. Usar `predict()`
  directo aplicaría el corte 0.5 por defecto y degradaría el f1_macro de 0.741 a
  0.631. La app aplica el umbral siempre.
- **Las versiones de las dependencias están fijadas** a las del entorno de
  entrenamiento (`requirements.txt` de esta carpeta) para que el joblib cargue sin
  incompatibilidades en la nube.
- `runtime.txt` fija Python 3.12, la versión usada en el proyecto.
- El score que muestra la app no es una probabilidad calibrada: el notebook de
  interpretación documenta que la correlación entre las bilirrubinas infla la
  confianza numérica del GaussianNB.
