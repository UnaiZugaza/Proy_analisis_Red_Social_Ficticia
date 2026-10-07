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
    pass  # TODO


def cargar_publicaciones(ruta_excel):
    """
    Recibe la ruta del libro de Excel de publicaciones.
    Devuelve un DataFrame con el contenido de la hoja 'publicaciones'.
    """
    pass  # TODO


def limpiar_dataset(df):
    """
    Recibe un DataFrame y devuelve una COPIA sin nulos: los nulos de las
    columnas numéricas se sustituyen por la mediana de su columna y los de
    las columnas de texto por 'Desconocido'. No debe modificar el original.
    """
    pass  # TODO