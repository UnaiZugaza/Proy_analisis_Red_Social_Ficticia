"""
pipeline.py
Script de entrega del proyecto Red Social Ficticia — IABD 2626-27

Instrucciones:
    - Implementa cada función según las especificaciones de su bloque.
    - No cambies los nombres ni las firmas de las funciones.
    - Ejecuta los tests de corrección con:
          python -m pytest tests/test_bloque1.py -v
          python -m pytest tests/test_bloque2.py -v
          python -m pytest tests/test_bloque3.py -v
          python -m pytest tests/test_bloque4.py -v
          python -m pytest tests/test_bloque5.py -v
          python -m pytest tests/ -v              # todos a la vez
"""

import os
import re

import numpy as np
import pandas as pd


# ============================================================
# BLOQUE 1 — Estructuras de datos, Regex y Lambda
# ============================================================

def usuarios_activos(lista_usuarios):
    """
    Recibe una lista de diccionarios con datos de usuarios (cargados desde CSV).
    Devuelve una lista con solo los usuarios cuyo campo 'activo' sea 'True' (string).
    """
    return [usuario for usuario in lista_usuarios if usuario.get("activo") == "True"]


def agrupar_por_ciudad(lista_usuarios):
    """
    Recibe una lista de diccionarios con datos de usuarios.
    Devuelve un diccionario {ciudad: [nombres_de_usuarios]}.
    Los usuarios sin ciudad (None o '') deben ignorarse.
    """
    grupo_ciudades = {}
    for usuario in lista_usuarios:
        ciudad = usuario.get("ciudad")
        if ciudad:
            if ciudad not in grupo_ciudades:
                grupo_ciudades[ciudad] = []
            grupo_ciudades[ciudad].append(usuario.get("nombre"))
    return grupo_ciudades


def hashtags_unicos(lista_publicaciones):
    """
    Recibe una lista de diccionarios con datos de publicaciones (cargados desde CSV).
    Cada publicación tiene 'hashtags': cadena separada por comas ('#ia,#python,...').
    Devuelve un set con todos los hashtags únicos del dataset.
    """
    hashtags = set()
    for pub in lista_publicaciones:
        pub_hashtags = pub.get("hashtags", "")
        if pub_hashtags:
            for tag in pub_hashtags.split(","):
                hashtags.add(tag.strip().lower())
    return hashtags


def top_por_seguidores(lista_usuarios, n=10):
    """
    Recibe una lista de diccionarios con datos de usuarios y un entero n.
    Devuelve una lista con los n usuarios con más seguidores (int), de mayor a menor.
    Debe usar sorted() con una función lambda como key.
    """
    return sorted(
        lista_usuarios,
        key=lambda u: int(u.get("seguidores", 0)),
        reverse=True
    )[:n]


def extraer_hashtags_regex(texto):
    """
    Recibe un texto y extrae sus hashtags mediante expresiones regulares.
    Devuelve una lista de hashtags en minúsculas y en el orden encontrado.
    Un hashtag está formado por '#' seguido de letras, números o '_'.
    """
    if not texto:
        return []
    patron = r'#\w+'
    return [h.lower() for h in re.findall(patron, texto)]


def publicaciones_con_hashtag(lista_publicaciones, hashtag):
    """
    Recibe publicaciones y un hashtag a buscar, por ejemplo '#ia'.
    Devuelve las publicaciones que lo contienen en el campo 'hashtags'.
    La búsqueda no distingue mayúsculas y no debe aceptar coincidencias parciales.
    Por ejemplo, '#ia' no coincide con '#iabd'.
    """
    patron = re.escape(hashtag) + r'(?!\w)'
    
    return [
        p for p in lista_publicaciones
        if p.get("hashtags") and re.search(patron, p.get("hashtags"), flags=re.IGNORECASE)
    ]

# ============================================================
# BLOQUE 2 — NumPy
# ============================================================

import numpy as np


def estadisticas_columna(arr):
    """
    Recibe un array de NumPy con valores numéricos.
    Devuelve un diccionario con las claves:
        'media', 'mediana', 'desv_std', 'minimo', 'maximo'
    Todos los valores deben ser float.
    """
    return {
        'media': float(np.mean(arr)),
        'mediana': float(np.median(arr)),
        'desv_std': float(np.std(arr)),
        'minimo': float(np.min(arr)),
        'maximo': float(np.max(arr))
    }


def resumen_publicaciones(matriz):
    """
    Recibe una matriz de NumPy de publicaciones por usuario (filas) y tipo
    de contenido (columnas), como la del ejercicio 5.
    Devuelve un diccionario con las claves:
        'total_por_usuario'         -> array con el total de publicaciones de cada usuario
        'total_por_tipo'            -> array con el total de publicaciones de cada tipo de contenido
        'usuario_mas_publicaciones' -> índice (int) del usuario con más publicaciones en total
    """
    total_por_usuario = matriz.sum(axis=1)
    total_por_tipo = matriz.sum(axis=0)
    usuario_mas_publicaciones = int(total_por_usuario.argmax())

    return {
        'total_por_usuario': total_por_usuario,
        'total_por_tipo': total_por_tipo,
        'usuario_mas_publicaciones': usuario_mas_publicaciones
    }


def contar_hashtags_array(textos):
    """
    Recibe un array (o lista) de NumPy de textos, como en el ejercicio 7.
    Devuelve un array con el número de hashtags (palabras que empiezan por '#')
    de cada texto, calculado con una función universal (ufunc) de NumPy en lugar
    de un bucle explícito sobre el array.
    """
    def contar(texto):
        return sum(1 for palabra in str(texto).split() if palabra.startswith('#'))

    ufunc_hashtags = np.frompyfunc(contar, 1, 1)
    return ufunc_hashtags(textos).astype(int)


def normalizar_minmax(arr):
    """
    Recibe un array de NumPy de una dimensión, como en el ejercicio 8.
    Devuelve un array normalizado entre 0 y 1 con la fórmula Min-Max:
        (valor - minimo) / (maximo - minimo)
    """
    minimo = arr.min()
    maximo = arr.max()
    return (arr - minimo) / (maximo - minimo)


def estandarizar_zscore(arr):
    """
    Recibe un array de NumPy de una dimensión, como en el ejercicio 8.
    Devuelve su Z-score: (valor - media) / desviación_estándar.
    Si la desviación estándar es 0, debe sustituirse por 1 antes de
    dividir, para evitar una división por cero.
    """
    media = arr.mean()
    desviacion = arr.std()
    desviacion_segura = np.where(desviacion == 0, 1.0, desviacion)
    return (arr - media) / desviacion_segura

# ============================================================
# BLOQUE 3 — Pandas básico
# ============================================================

def cargar_usuarios(ruta_csv):
    """
    Recibe la ruta del fichero CSV de usuarios.
    Devuelve un DataFrame con su contenido.
    """
    return pd.read_csv(ruta_csv)


def cargar_publicaciones(ruta_excel):
    """
    Recibe la ruta del libro de Excel de publicaciones.
    Devuelve un DataFrame con el contenido de la hoja 'publicaciones'.
    """
    return pd.read_excel(ruta_excel, sheet_name='publicaciones')


def limpiar_dataset(df):
    """
    Recibe un DataFrame y devuelve una COPIA sin nulos: los nulos de las
    columnas numéricas se sustituyen por la mediana de su columna y los de
    las columnas de texto por 'Desconocido'. No debe modificar el original.
    """
    df_copia = df.copy()

    columnas_numericas = df_copia.select_dtypes(include=[np.number]).columns
    for col in columnas_numericas:
        df_copia[col] = df_copia[col].fillna(df_copia[col].median())

    columnas_texto = df_copia.select_dtypes(include=['object', 'string']).columns
    for col in columnas_texto:
        df_copia[col] = df_copia[col].fillna('Desconocido')

    return df_copia


# ============================================================
# BLOQUE 4 — Pandas avanzado
# ============================================================

def calcular_engagement(df):
    """
    Recibe un DataFrame con las columnas 'likes', 'comentarios',
    'compartidos' y 'visualizaciones'. Devuelve una COPIA con la columna
    'engagement_rate' = (likes + comentarios + compartidos) / visualizaciones.
    Si 'visualizaciones' es 0, el engagement debe ser 0 (nunca nulo ni
    infinito). No modifica el DataFrame original.
    """
    df_copia = df.copy()
    interacciones = df_copia['likes'] + df_copia['comentarios'] + df_copia['compartidos']
    
    df_copia['engagement_rate'] = np.where(
        df_copia['visualizaciones'] > 0,
        interacciones / df_copia['visualizaciones'],
        0.0
    )
    return df_copia


def top_creadores(df_merged, n=10):
    """
    Recibe el DataFrame combinado (con 'engagement_rate') y un entero n.
    Devuelve un DataFrame con UNA fila por usuario y las columnas
    'id_usuario', 'nombre', 'tipo_cuenta' y 'engagement_promedio' (media de
    'engagement_rate' del usuario), ordenado de mayor a menor y limitado a
    n filas. Un usuario se identifica por su 'id_usuario' (hay nombres
    repetidos).
    """
    return (
        df_merged.groupby(['id_usuario', 'nombre', 'tipo_cuenta'], observed=True)['engagement_rate']
        .mean()
        .reset_index(name='engagement_promedio')
        .sort_values(by='engagement_promedio', ascending=False)
        .head(n)
    )


def resumen_por_ciudad(df_merged):
    """
    Recibe el DataFrame combinado (con 'engagement_rate'). Devuelve un
    DataFrame con una fila por ciudad (la ciudad es el índice) y las
    columnas 'media_seguidores' (media de 'seguidores' de las filas de esa
    ciudad), 'n_publicaciones' (número de filas) y 'engagement_promedio',
    ordenado por 'n_publicaciones' de mayor a menor.
    """
    return (
        df_merged.groupby('ciudad')
        .agg(
            media_seguidores=('seguidores', 'mean'),
            n_publicaciones=('id_publicacion', 'count'),
            engagement_promedio=('engagement_rate', 'mean')
        )
        .sort_values(by='n_publicaciones', ascending=False)
    )


def guardar_parquet(df, ruta):
    """
    Guarda el DataFrame 'df' en formato Parquet en 'ruta' con compresión
    'snappy' y sin incluir el índice. Debe crear las carpetas intermedias
    que falten. No devuelve nada (None).
    """
    directorio = os.path.dirname(ruta)
    if directorio:
        os.makedirs(directorio, exist_ok=True)
        
    df.to_parquet(ruta, engine='pyarrow', compression='snappy', index=False)
    return None

# ============================================================
# BLOQUE 5 — Visualización y Faker
# ============================================================

import os
import random
from datetime import date

import pandas as pd
import plotly.graph_objects as go
from faker import Faker
from plotly.subplots import make_subplots


def exportar_grafico(fig, ruta_html, ruta_png=None):
    """
    Exporta la figura de Plotly 'fig' a un fichero HTML interactivo en
    'ruta_html'. Si se indica 'ruta_png', exporta también una imagen PNG
    (requiere kaleido). Debe crear las carpetas intermedias que falten. No
    devuelve nada (None).
    """
    dir_html = os.path.dirname(ruta_html)
    if dir_html:
        os.makedirs(dir_html, exist_ok=True)
    fig.write_html(ruta_html)

    if ruta_png is not None:
        dir_png = os.path.dirname(ruta_png)
        if dir_png:
            os.makedirs(dir_png, exist_ok=True)
        fig.write_image(ruta_png)

    return None


def publicaciones_por_mes(df):
    """
    Recibe un DataFrame de publicaciones con la columna 'fecha' (texto
    'AAAA-MM-DD' o tipo fecha). Devuelve un DataFrame con las columnas 'mes'
    (formato 'AAAA-MM') y 'publicaciones' (número de publicaciones de ese
    mes), ordenado cronológicamente y con índice 0, 1, 2...
    """
    df_temp = df.copy()
    df_temp['mes'] = df_temp['fecha'].astype(str).str[:7]

    resumen = (
        df_temp.groupby('mes', as_index=False)
        .size()
        .rename(columns={'size': 'publicaciones'})
        .sort_values(by='mes')
        .reset_index(drop=True)
    )
    return resumen


def crear_dashboard(df):
    """
    Recibe un DataFrame de publicaciones con sus autores (columnas 'ciudad',
    'tipo_cuenta', 'fecha' y 'likes') y devuelve una figura de Plotly con un
    panel de 2 x 2 gráficos:
        [fila 1, col 1] barras: publicaciones de las 8 ciudades con más
                        publicaciones (de mayor a menor)
        [fila 1, col 2] sectores: publicaciones de cada 'tipo_cuenta'
        [fila 2, col 1] líneas con marcadores: publicaciones por mes
        [fila 2, col 2] histograma de 'likes'
    La figura mide 800 píxeles de alto, se titula 'Dashboard Red Social
    Ficticia', usa la plantilla 'plotly_white' y no muestra leyenda. No debe
    modificar el DataFrame original.
    """
    df_local = df.copy()
    df_local['mes'] = df_local['fecha'].astype(str).str[:7]

    pubs_ciudad = (
        df_local['ciudad']
        .value_counts()
        .head(8)
        .reset_index()
    )
    pubs_ciudad.columns = ['ciudad', 'publicaciones']

    cuentas = df_local['tipo_cuenta'].value_counts()

    pubs_mes = (
        df_local.groupby('mes', as_index=False)
        .size()
        .rename(columns={'size': 'publicaciones'})
        .sort_values(by='mes')
        .reset_index(drop=True)
    )

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Publicaciones por Ciudad',
            'Distribución por Tipo de Cuenta',
            'Publicaciones por Mes',
            'Distribución de Likes'
        ),
        specs=[[{"type": "xy"}, {"type": "domain"}],
               [{"type": "xy"}, {"type": "xy"}]]
    )

    fig.add_trace(
        go.Bar(x=pubs_ciudad['ciudad'], y=pubs_ciudad['publicaciones']),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=cuentas.index, values=cuentas.values),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=pubs_mes['mes'], y=pubs_mes['publicaciones'], mode='lines+markers'),
        row=2, col=1
    )

    fig.add_trace(
        go.Histogram(x=df_local['likes']),
        row=2, col=2
    )

    fig.update_layout(
        height=800,
        title_text='Dashboard Red Social Ficticia',
        template='plotly_white',
        showlegend=False
    )

    return fig


def generar_datos_demo(n=10, seed=2024):
    """
    Genera n usuarios ficticios con Faker en español y devuelve un DataFrame
    con las columnas 'nombre', 'apellidos' (dos apellidos), 'email',
    'ciudad', 'telefono' y 'fecha_registro' (texto 'AAAA-MM-DD' entre
    2018-01-01 y 2024-06-01). Es REPRODUCIBLE: con la misma 'seed' devuelve
    siempre los mismos datos. Con n <= 0 devuelve una tabla vacía con esas
    columnas.
    """
    columnas = ['nombre', 'apellidos', 'email', 'ciudad', 'telefono', 'fecha_registro']
    if n <= 0:
        return pd.DataFrame(columns=columnas)

    fake = Faker('es_ES')
    Faker.seed(seed)
    random.seed(seed)

    datos = []
    fecha_inicio = date(2018, 1, 1)
    fecha_fin = date(2024, 6, 1)

    for _ in range(n):
        datos.append({
            'nombre': fake.first_name(),
            'apellidos': f"{fake.last_name()} {fake.last_name()}",
            'email': fake.email(),
            'ciudad': fake.city(),
            'telefono': fake.phone_number(),
            'fecha_registro': fake.date_between(start_date=fecha_inicio, end_date=fecha_fin).strftime('%Y-%m-%d')
        })

    return pd.DataFrame(datos)


def ampliar_dataset(df_usuarios, n_nuevos):
    """
    Recibe la tabla de usuarios y un entero n_nuevos. Devuelve un DataFrame
    con los usuarios originales (sin cambios y al principio) seguidos de
    n_nuevos usuarios ficticios generados con Faker en español:
      - 'id_usuario' continúa desde el máximo existente + 1 (sin repetirse)
      - mismas columnas, orden y tipos de dato que la tabla original
      - 'tipo_cuenta': 60% free, 30% premium y 10% creator
      - 'seguidores': entre 1000 y 50000 si es creator, entre 10 y 5000 si no
      - 'edad' entre 18 y 55; 'ciudad', 'pais' y 'genero' se eligen entre los
        valores que ya existen en la tabla original
    Con n_nuevos <= 0 devuelve una copia de la tabla original.
    """
    if n_nuevos <= 0:
        return df_usuarios.copy()

    fake = Faker('es_ES')
    Faker.seed(2024)
    random.seed(2024)

    ciudades = df_usuarios['ciudad'].dropna().unique().tolist()
    paises = df_usuarios['pais'].dropna().unique().tolist()
    generos = df_usuarios['genero'].dropna().unique().tolist()

    id_max = int(df_usuarios['id_usuario'].max()) if len(df_usuarios) > 0 else 0

    fecha_inicio = date(2018, 1, 1)
    fecha_fin = date(2024, 6, 1)

    nuevos = []
    for i in range(n_nuevos):
        tipo = random.choices(['free', 'premium', 'creator'], weights=[60, 30, 10], k=1)[0]
        seguidores = random.randint(1000, 50000) if tipo == 'creator' else random.randint(10, 5000)

        usuario = {
            'id_usuario': id_max + 1 + i,
            'nombre': fake.first_name(),
            'apellidos': f"{fake.last_name()} {fake.last_name()}",
            'edad': float(random.randint(18, 55)),
            'ciudad': random.choice(ciudades),
            'pais': random.choice(paises),
            'genero': random.choice(generos),
            'fecha_registro': fake.date_between(start_date=fecha_inicio, end_date=fecha_fin).strftime('%Y-%m-%d'),
            'tipo_cuenta': tipo,
            'seguidores': seguidores,
            'seguidos': random.randint(20, 1000),
            'publicaciones_totales': random.randint(0, 500),
            'activo': random.random() < 0.8,
            'bio': fake.sentence()
        }
        nuevos.append(usuario)

    df_nuevos = pd.DataFrame(nuevos)

    df_nuevos = df_nuevos[df_usuarios.columns]
    for col in df_usuarios.columns:
        df_nuevos[col] = df_nuevos[col].astype(df_usuarios[col].dtype)

    return pd.concat([df_usuarios, df_nuevos], ignore_index=True)