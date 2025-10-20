#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import json
import ast
from flask import Flask, request, jsonify

"""
Muchas veces el json que viene en un request no tiene el formato adecuado, por
ej. por no tener las comillas adecuados y esto hace que al convertirlo a objeto
de error.
Esta funcion se encarga de corregirlo
"""

def tolerant_json_load(raw_body: str):
    """
    Intenta parsear un JSON que puede venir mal formado:
    - Primero intenta json.loads() (JSON estándar)
    - Luego ast.literal_eval() (dict de Python con comillas simples)
    - Finalmente intenta un reemplazo de comillas simples a dobles
    """
    reparado = False
    raw_body = raw_body.strip()

    # Primer intento: JSON válido
    try:
        return json.loads(raw_body), reparado
    except json.JSONDecodeError:
        pass

    # Segundo intento: dict estilo Python
    try:
        parsed = ast.literal_eval(raw_body)
        if isinstance(parsed, (dict, list)):
            reparado = True
            return parsed, reparado
    except Exception:
        pass

    # Último recurso: reemplazar comillas simples por dobles
    try:
        fixed = raw_body.replace("'", '"')
        reparado = True
        return json.loads(fixed), reparado 
    except Exception as e:
        raise ValueError(f"No se pudo parsear el JSON: {e}")