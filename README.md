# Proyecto: Análisis de una Red Social Ficticia

> **Curso de Especialización en Inteligencia Artificial y Big Data (IABD) — Curso 2026/2027**  
> **Módulo:** Programación y Análisis de Datos con Python

---

## 1. ¿De qué trata este proyecto?

En este proyecto construirás un **pipeline de ingeniería y análisis de datos en Python** de principio a fin, trabajando sobre el ecosistema de una red social ficticia compuesta por perfiles de usuarios, publicaciones e interacciones, y un grafo de conexiones de seguidores.

El proyecto está diseñado de forma **incremental y modular**: a medida que avances en las clases y en los cuadernos de apuntes teóricos, desbloquearás un **Bloque de Cuaderno Jupyter** para practicar interactivamente y trasladarás las funciones clave a `scripts/pipeline.py`, donde se validarán automáticamente con pruebas unitarias (`pytest`).

```
                    ┌──────────────────────────────┐
                    │    Cuadernos de Apuntes      │
                    │   (Fundamentos teóricos)     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Cuadernos de Bloque (.ipynb)│
                    │    (Práctica interactiva)    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    ?  Entrega en scripts/pipeline.py  ?
                    │   (Código limpio y modular)  │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Validación con pytest       │
                    │    (Tests automatizados)     │
                    └──────────────────────────────┘
```

---

## 2. Estructura del Repositorio: ¿Qué es cada archivo?

| Archivo / Carpeta | ¿Para qué sirve? |
|---|---|
| `README.md` | Guía del proyecto, explicación del flujo de trabajo y enunciados para el alumno. |
| `data/setup_datos.py` | Script generador que crea los datasets iniciales (`usuarios.csv`, `publicaciones.csv`, `publicaciones.xlsx`, `conexiones.json`). |
| `scripts/pipeline.py` | **Tu archivo principal de entrega.** Aquí implementarás las funciones estándar solicitadas en cada bloque. |
| `scripts/pipeline_avanzada.py` | Archivo de entrega complementario para ejercicios y retos avanzados con tipado estático (`typing`). |
| `scripts/generate_notebooks.py` | Script que permite recrear y sincronizar los 5 cuadernos Jupyter en `notebooks/` si se requiere un reseteo limpio. |
| `notebooks/Bloque_01_EstructurasDatos_Lambda.ipynb` | Cuaderno de ejercicios del Bloque 1 (Librería estándar, listas, diccionarios, sets y lambda). |
| `notebooks/Bloque_02_NumPy.ipynb` | Cuaderno de ejercicios del Bloque 2 (NumPy, arrays, álgebra y vectorización). |
| `notebooks/Bloque_03_Pandas_Basico.ipynb` | Cuaderno de ejercicios del Bloque 3 (Pandas básico: DataFrames, carga multiformato, filtros y limpieza). |
| `notebooks/Bloque_04_Pandas_Avanzado.ipynb` | Cuaderno de ejercicios del Bloque 4 (Pandas avanzado: tipos category, codificación, groupby, merge y Parquet). |
| `notebooks/Bloque_05_Graficos_Faker.ipynb` | Cuaderno de ejercicios del Bloque 5 (Visualización interactiva con Plotly y generación masiva con Faker). |
| `tests/` | Batería de pruebas automatizadas con `pytest` para verificar tus funciones de forma inmediata. |
| `output_graficos/` | Carpeta donde se guardarán automáticamente tus gráficos interactivos (`.html`) y estáticos (`.png`). |

---

## 3. Preparación Inicial del Entorno

Antes de comenzar a programar, sigue estos sencillos pasos:

### Paso 1: Instalar las dependencias
Este proyecto gestiona el entorno virtual y las dependencias con [uv](https://docs.astral.sh/uv/). Abre una terminal en VS Code, en la carpeta del proyecto, y ejecuta:
```powershell
uv sync
```
Esto crea automáticamente la carpeta `.venv` e instala todas las librerías necesarias (`numpy`, `pandas`, `openpyxl`, `pyarrow`, `fastparquet`, `plotly`, `kaleido`, `faker`, `pytest`) según `pyproject.toml`.

Para ejecutar cualquier script o notebook dentro del entorno sin activarlo manualmente:
```powershell
uv run python data/setup_datos.py
uv run pytest tests/ -v
```

### Paso 2: Generar los datos base
Crea los archivos de prueba ejecutando el script generador:
```powershell
python data/setup_datos.py
```
> Esto creará en la carpeta `data/` los perfiles de usuario, las publicaciones y el grafo de conexiones.

---

## 4. Guía Paso a Paso: Itinerario de Trabajo por Temas

Cada bloque del proyecto se realiza en **3 fases**:
1. **Estudio:** Repasar el tema correspondiente en la carpeta de apuntes.
2. **Experimentación:** Abrir el cuaderno `.ipynb` del bloque y resolver las celdas guiadas.
3. **Entrega y Test:** Trasladar la solución a la función correspondiente en `scripts/pipeline.py` y ejecutar el test unitario.

---

### 🔹 Bloque 1 — Estructuras de Datos Nativas y Funciones Lambda
* **Temas asociados en Apuntes:** `06_Listas`, `07_Diccionarios`, `08_Conjuntos`, `09_Tuplas`, `11_Funciones_lambda`, `15_Expresiones regulares`.
* **Cuaderno:** `notebooks/Bloque_01_EstructurasDatos_Lambda.ipynb`
* **Regla estricta:** Solo se permite usar la librería estándar de Python (`csv`, `json`, `collections`, `re`, `functools`). **Prohibido importar Pandas o NumPy en este bloque.**
* **Funciones a implementar en `scripts/pipeline.py`:**
  - `usuarios_activos(lista_usuarios)`: Filtra usuarios activos (`activo == 'True'`).
  - `agrupar_por_ciudad(lista_usuarios)`: Retorna diccionario `{ciudad: [nombres]}` ignorando vacíos.
  - `hashtags_unicos(lista_publicaciones)`: Retorna un `set` con todos los hashtags únicos.
  - `top_por_seguidores(lista_usuarios, n=10)`: Retorna el top $n$ de usuarios ordenados por seguidores mediante `sorted()` y `lambda`.
  - `extraer_hashtags_regex(texto)`: Extrae lista de hashtags en minúsculas con expresiones regulares.
  - `publicaciones_con_hashtag(lista_publicaciones, hashtag)`: Filtra publicaciones que contienen un hashtag exacto.
* **Comprobación:**
  ```powershell
  python -m pytest tests/test_bloque1.py -v
  ```

---

### 🔹 Bloque 2 — Cálculo Vectorial con NumPy
* **Temas asociados en Apuntes:** `21_Numpy`.
* **Cuaderno:** `notebooks/Bloque_02_NumPy.ipynb`
* **Regla estricta:** Todos los cálculos matemáticos deben ser vectorizados sobre arrays (`np.ndarray`). **Prohibido el uso de bucles `for` o `while` en operaciones numéricas.**
* **Funciones a implementar en `scripts/pipeline.py`:**
  - `estadisticas_columna(arr)`: Retorna diccionario con media, mediana, desviación estándar, mínimo y máximo como floats.
* **Comprobación:**
  ```powershell
  python -m pytest tests/test_bloque2.py -v
  ```

---

### 🔹 Bloque 3 — Ingesta, Limpieza y Pandas Básico
* **Temas asociados en Apuntes:** `22_Pandas_dataframes (I)`, `23_Pandas_dataframes (II)_herramientas`, `24_Pandas_dataframes (III)_series`.
* **Cuaderno:** `notebooks/Bloque_03_Pandas_Basico.ipynb`
* **Objetivo:** Manipulación tabular, selección con `.loc` / `.iloc`, filtros booleanos, accesores `.str` / `.dt` y tratamiento de valores ausentes.
* **Funciones a implementar en `scripts/pipeline.py`:**
  - `cargar_usuarios(ruta_csv)`: Carga el fichero de usuarios con `pd.read_csv`.
  - `cargar_publicaciones(ruta_excel)`: Carga la hoja `'publicaciones'` de Excel con `pd.read_excel`.
  - `limpiar_dataset(df)`: Imputa nulos con la mediana en columnas numéricas y con `'Desconocido'` en columnas de texto sin mutar el DataFrame original (`df.copy()`).
* **Comprobación:**
  ```powershell
  python -m pytest tests/test_bloque3.py -v
  ```

---

### 🔹 Bloque 4 — Métricas de Negocio, Agrupaciones y Parquet
* **Temas asociados en Apuntes:** `25_Pandas dataframes (IV)_VarCategoricas`, `26_Pandas_dataframes (V)_Agrupaciones_y_combinaciones`.
* **Cuaderno:** `notebooks/Bloque_04_Pandas_Avanzado.ipynb`
* **Objetivo:** Variables categóricas, tablas dinámicas, cruces relacionales y exportación columnar Parquet.
* **Funciones a implementar en `scripts/pipeline.py`:**
  - `calcular_engagement(df)`: Añade la métrica `engagement_rate = (likes + comentarios + compartidos) / visualizaciones` controlando la división por cero cuando `visualizaciones == 0`.
  - `top_creadores(df_merged, n=10)`: Retorna los $n$ usuarios con mayor engagement promedio ordenados de forma descendente.
  - `resumen_por_ciudad(df_merged)`: Agrupa por ciudad resumiendo media de seguidores, total de publicaciones y engagement promedio.
  - `guardar_parquet(df, ruta)`: Guarda el DataFrame combinado en formato Apache Parquet con compresión `snappy`.
* **Comprobación:**
  ```powershell
  python -m pytest tests/test_bloque4.py -v
  ```

---

### 🔹 Bloque 5 — Visualización con Plotly y Escalado con Faker
* **Temas asociados en Apuntes:** `27_Graficos`, `28_Faker`.
* **Cuaderno:** `notebooks/Bloque_05_Graficos_Faker.ipynb`
* **Objetivo:** Visualización analítica interactiva y generación sintética de datos.
* **Funciones a implementar en `scripts/pipeline.py`:**
  - `exportar_grafico(fig, ruta_html, ruta_png=None)`: Exporta una figura de Plotly a archivo HTML interactivo y opcionalmente a PNG estático.
  - `ampliar_dataset(df_usuarios, n_nuevos)`: Genera $n$ perfiles sintéticos adicionales mediante Faker conservando exactamente el esquema de columnas y tipos de `usuarios.csv`.
* **Comprobación:**
  ```powershell
  python -m pytest tests/test_bloque5.py -v
  ```

---

## 5. Comprobación Global de la Entrega

Para comprobar que todo tu pipeline funciona correctamente y supera el 100% de las validaciones, ejecuta:

```powershell
python -m pytest tests/ -v
```

Si deseas abordar la modalidad con tipado estático y ejercicios avanzados de arquitectura:
```powershell
python -m pytest tests/*_avanzado.py -v
```

---

## 6. Buenas Prácticas y Consejos

1. **Inmutabilidad:** No modifiques nunca los DataFrames pasados por argumento. Realiza siempre `df_copia = df.copy()` al inicio de tus funciones.
2. **Tipos de datos:** Ten en cuenta que los archivos CSV leen todos los campos como cadenas de texto (`str`). Convierte explícitamente a `int` o `float` cuando trabajes en el Bloque 1.
3. **Idempotencia:** Asegúrate de que tus funciones produzcan el mismo resultado independientemente de cuántas veces sean ejecutadas.
