from flask import jsonify, request
import requests
import jwt
from functools import wraps
from config import SECRET_KEY, TAREAS_API


# -------------------------
# TOKEN REQUERIDO
# -------------------------
def token_requerido(f):

    @wraps(f)
    def decorador(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:

            return jsonify({
                "error": "Token requerido"
            }), 401

        try:

            # Quitar Bearer
            if " " in token:
                token = token.split(" ")[1]

            usuario = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

        except Exception as e:

            print("ERROR TOKEN:", e)

            return jsonify({
                "error": "Token inválido"
            }), 401

        return f(usuario, *args, **kwargs)

    return decorador


# -------------------------
# SOLO ADMIN
# -------------------------
def admin_requerido(f):

    @wraps(f)
    def decorador(usuario, *args, **kwargs):

        if usuario.get("rol") != "admin":

            return jsonify({
                "error": "Solo administradores"
            }), 403

        return f(usuario, *args, **kwargs)

    return decorador


# -------------------------
# OBTENER TAREAS
# -------------------------
def obtener_tareas(headers):

    try:

        response = requests.get(
            TAREAS_API,
            headers=headers,
            timeout=5
        )

        print("STATUS TAREAS:", response.status_code)

        datos = response.json()

        print("DATOS TAREAS:", datos)

        tareas = datos.get("tareas", [])

        return tareas

    except Exception as e:

        print("ERROR OBTENIENDO TAREAS:", e)

        return []


# -------------------------
# ROUTES
# -------------------------
def register_routes(app):


    # --------------------------------
    # DASHBOARD GENERAL
    # --------------------------------
    @app.route('/dashboard', methods=['GET'])
    @token_requerido
    @admin_requerido
    def dashboard(usuario):

        headers = {
            "Authorization": request.headers.get("Authorization")
        }

        tareas = obtener_tareas(headers)

        total = len(tareas)

        completadas = len([
            t for t in tareas
            if t.get("completada")
        ])

        pendientes = total - completadas

        porcentaje = 0

        if total > 0:

            porcentaje = round(
                (completadas / total) * 100,
                2
            )

        return jsonify({

            "metricas_generales": {

                "total_tareas": total,

                "tareas_completadas": completadas,

                "tareas_pendientes": pendientes,

                "porcentaje_completado": porcentaje
            }
        })


    # --------------------------------
    # PRODUCTIVIDAD POR USUARIO
    # --------------------------------
    @app.route('/productividad', methods=['GET'])
    @token_requerido
    @admin_requerido
    def productividad(usuario):

        headers = {
            "Authorization": request.headers.get("Authorization")
        }

        tareas = obtener_tareas(headers)

        productividad = {}

        for tarea in tareas:

            usuario_id = tarea.get("usuario_id")

            if usuario_id not in productividad:

                productividad[usuario_id] = {

                    "total": 0,

                    "completadas": 0
                }

            productividad[usuario_id]["total"] += 1

            if tarea.get("completada"):

                productividad[usuario_id]["completadas"] += 1

        return jsonify(productividad)


    # --------------------------------
    # TAREAS COMPLETADAS
    # --------------------------------
    @app.route('/completadas', methods=['GET'])
    @token_requerido
    @admin_requerido
    def completadas(usuario):

        headers = {
            "Authorization": request.headers.get("Authorization")
        }

        tareas = obtener_tareas(headers)

        completadas = [

            t for t in tareas

            if t.get("completada")
        ]

        return jsonify({

            "cantidad_completadas": len(completadas)
        })


    # --------------------------------
    # ESTADÍSTICAS EXTRA
    # --------------------------------
    @app.route('/estadisticas', methods=['GET'])
    @token_requerido
    @admin_requerido
    def estadisticas(usuario):

        headers = {
            "Authorization": request.headers.get("Authorization")
        }

        tareas = obtener_tareas(headers)

        total = len(tareas)

        completadas = len([
            t for t in tareas
            if t.get("completada")
        ])

        pendientes = total - completadas

        porcentaje = 0

        if total > 0:

            porcentaje = round(
                (completadas / total) * 100,
                2
            )

        return jsonify({

            "total_tareas": total,

            "completadas": completadas,

            "pendientes": pendientes,

            "porcentaje": porcentaje
        })