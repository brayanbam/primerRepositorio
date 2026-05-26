from flask import request, jsonify
from db import get_connection
import jwt
from functools import wraps
from config import SECRET_KEY, NOTIFICACIONES_TOKEN


# DECORADOR PARA TOKEN

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token no enviado"}), 401
        try:
            if " " in token:
                token = token.split(" ")[1]
        except:
            return jsonify({"error": "Formato de token inválido"}), 401

        if token == NOTIFICACIONES_TOKEN:
            usuario = {"id_usuario": 0, "rol": "admin"}
        else:
            try:
                usuario = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except Exception:
                return jsonify({"error": "Token inválido o expirado"}), 401

        return f(usuario, *args, **kwargs)
    return decorador


# DECORADOR PARA ADMIN

def admin_requerido(f):
    @wraps(f)
    def decorador(usuario_actual, *args, **kwargs):
        if usuario_actual.get("rol") != "admin":
            return jsonify({"error": "Solo los administradores pueden realizar esta acción"}), 403
        return f(usuario_actual, *args, **kwargs)
    return decorador

# RUTAS

def register_routes(app):

    @app.route('/tareas', methods=['GET'])
    @token_requerido
    def obtener_tareas(usuario_actual):
        conn = get_connection()
        try:
            c = conn.cursor()
            if usuario_actual.get("rol") == "admin":
                c.execute("SELECT * FROM tareas")
            else:
                c.execute("SELECT * FROM tareas WHERE usuario_id = ?", (usuario_actual.get("id_usuario"),))
            
            tareas = [{
                "id": r[0],
                "usuario_id": r[1],
                "titulo": r[2],
                "descripcion": r[3],
                "completada": bool(r[4]),
                "intervalo_notificacion": r[5]
            } for r in c.fetchall()]
        finally:
            conn.close()

        return jsonify({"tareas": tareas}), 200

    @app.route('/tareas', methods=['POST'])
    @token_requerido
    @admin_requerido
    def crear_tarea(usuario_actual):
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        usuario_id = data.get("usuario_id")
        titulo = data.get("titulo")
        descripcion = data.get("descripcion", "")
        intervalo = data.get("intervalo_notificacion", 60)

        if usuario_id is None or not titulo:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Evitar que un admin se asigne tarea a sí mismo (si id_usuario=0 es token notificaciones)
        if usuario_id == usuario_actual.get("id_usuario") and usuario_actual.get("id_usuario") != 0:
            return jsonify({"error": "No puedes asignarte tareas a ti mismo"}), 400

        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("""
                INSERT INTO tareas (usuario_id, titulo, descripcion, intervalo_notificacion)
                VALUES (?, ?, ?, ?)
            """, (usuario_id, titulo, descripcion, intervalo))
            conn.commit()
        finally:
            conn.close()

        return jsonify({"mensaje": "Tarea creada exitosamente"}), 201

    @app.route('/tareas/<int:id>/completar', methods=['PUT'])
    @token_requerido
    def completar_tarea(usuario_actual, id):
        usuario_id = usuario_actual.get("id_usuario")

        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("""
                UPDATE tareas SET completada = 1
                WHERE id = ? AND usuario_id = ?
            """, (id, usuario_id))
            if c.rowcount == 0:
                return jsonify({"error": "No puedes completar esta tarea o no existe"}), 403
            conn.commit()
        finally:
            conn.close()

        return jsonify({"mensaje": "Tarea marcada como completada"}), 200
