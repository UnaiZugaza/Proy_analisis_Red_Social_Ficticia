"""Plantilla de ejercicios avanzados del proyecto Red Social Ficticia.

Implementa cada funcion sin cambiar su nombre, firma ni tipo de retorno.
Ejecuta la correccion con ``python -m pytest tests/*_avanzado.py -v``.
"""

from typing import Any


# Bloque 1: estructuras de datos y lambda

def informe_actividad_ciudades(lista_usuarios: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Resume usuarios, activos y seguidores por ciudad."""
    usuarios_por_ciudad = {}

    for usuario in lista_usuarios:
        if usuario.get('ciudad'):
            ciudad = usuario.get('ciudad')
            if ciudad not in usuarios_por_ciudad:
                usuarios_por_ciudad[ciudad] = []
            usuarios_por_ciudad[ciudad].append(usuario)

    diccionario_por_ciudad = {}

    for ciudad, lista_usuarios in usuarios_por_ciudad.items():

        num_usuarios = len(lista_usuarios)
        activos = lambda lista: sum(1 for u in lista if u.get("activo", 'True') == 'True')
        seg_tot = lambda lista: sum(int(u.get("seguidores", 0)) for u in lista)

        diccionario_por_ciudad[ciudad] = {
            'usuarios': num_usuarios,
            'activos': activos(lista_usuarios),
            'seguidores_totales': seg_tot(lista_usuarios),
        }

    return diccionario_por_ciudad


def recomendaciones_por_conexiones(lista_usuarios: list[dict[str, Any]], conexiones: list[dict[str, Any]], id_usuario: int, limite: int = 5) -> list[dict[str, Any]]:
    """Devuelve personas seguidas por contactos pero no por el usuario."""
    mapa_usuarios = {int(u["id_usuario"]): u for u in lista_usuarios if "id_usuario" in u}

    mapa_siguiendo = {
        int(c["id_usuario"]): set(c.get("siguiendo", [])) 
        for c in conexiones if "id_usuario" in c
    }

    siguiendo_actual = mapa_siguiendo.get(id_usuario, set())

    candidatos = set()
    for contacto in siguiendo_actual:
        candidatos.update(mapa_siguiendo.get(contacto, set()))

    candidatos_validos = candidatos - siguiendo_actual - {id_usuario}

    ids_ordenados = sorted(
        candidatos_validos,
        key=lambda uid: int(mapa_usuarios[uid].get("seguidores", 0)) if uid in mapa_usuarios else 0,
        reverse=True
    )

    return [mapa_usuarios[uid] for uid in ids_ordenados if uid in mapa_usuarios][:limite]


def hashtags_normalizados(lista_publicaciones: list[dict[str, Any]]) -> set[str]:
    """Normaliza hashtags, elimina espacios y devuelve los valores unicos."""
    unicos = set()

    for pub in lista_publicaciones:
        cadena = pub.get("hashtags", "")
        if not cadena:
            continue

        for parte in str(cadena).split(","):
            limpio = parte.replace(" ", "").strip().lower()

            if not limpio or limpio == "#":
                continue

            if not limpio.startswith("#"):
                limpio = f"#{limpio}"

            unicos.add(limpio)

    return unicos


def validar_publicaciones(lista_publicaciones: list[dict[str, Any]], lista_usuarios: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separa publicaciones validas y publicaciones con usuario inexistente."""
    usuarios_validos = {int(u["id_usuario"]) for u in lista_usuarios if "id_usuario" in u}
    validas = []
    invalidas = []
    for pub in lista_publicaciones:
        if "id_usuario" in pub and int(pub["id_usuario"]) in usuarios_validos:
            validas.append(pub)
        else:
            invalidas.append(pub)
    return validas, invalidas