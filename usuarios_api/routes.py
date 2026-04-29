from flask import request, jsonify
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from config import SECRET_KEY, NOTIFICACIONES_TOKEN

# -------------------
# DECORADOR JWT
# -------------------
def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token no enviado'}), 401
        try:
            if " " in token:
                token = token.split(" ")[1]
        except:
            return jsonify({'error': 'Formato de token inválido'}), 401

        # Acceso especial para la API de notificaciones
        if token == NOTIFICACIONES_TOKEN:
            usuario = {"id_usuario": 0, "rol": "admin"}  # acceso completo
        else:
            try:
                usuario = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except Exception:
                return jsonify({'error': 'Token inválido o expirado'}), 401

        return f(usuario, *args, **kwargs)
    return decorador

# -------------------
# DECORADOR ADMIN
# -------------------
def admin_requerido(f):
    @wraps(f)
    def decorador(usuario_actual, *args, **kwargs):
        if usuario_actual.get("rol") != "admin" and usuario_actual.get("id_usuario") != 0:
            return jsonify({"error": "No tienes permisos de administrador"}), 403
        return f(usuario_actual, *args, **kwargs)
    return decorador

# -------------------
# RUTAS
# -------------------
def register_routes(app):
    # LOGIN
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT id, nombre, email, password, rol FROM usuarios WHERE email = ?", (email,))
            user = c.fetchone()
        finally:
            conn.close()

        if user and check_password_hash(user[3], password):
            token = jwt.encode({
                'id_usuario': user[0],
                'nombre': user[1],
                'email': user[2],
                'rol': user[4],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({
                'token': token,
                'usuario': {
                    "id": user[0],
                    "nombre": user[1],
                    "email": user[2],
                    "rol": user[4]
                }
            }), 200
        return jsonify({'error': 'Credenciales inválidas'}), 401

    # OBTENER TODOS LOS USUARIOS (solo admin o NOTIFICACIONES_TOKEN)
    @app.route('/usuarios', methods=['GET'])
    @token_requerido
    @admin_requerido
    def get_usuarios(usuario_actual):
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT id, nombre, email, chat_id, rol FROM usuarios")
            usuarios = [{"id": r[0], "nombre": r[1], "email": r[2], "chat_id": r[3], "rol": r[4]} for r in c.fetchall()]
        finally:
            conn.close()
        return jsonify({"usuarios": usuarios}), 200

    # CREAR USUARIO (registro público)
    @app.route('/usuarios', methods=['POST'])
    def crear_usuario():
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        nombre = data.get('nombre')
        email = data.get('email')
        password_plain = data.get('password')
        chat_id = data.get('chat_id')

        if not nombre or not email or not password_plain:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        password_hash = generate_password_hash(password_plain, method='pbkdf2:sha256')

        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO usuarios (nombre, email, password, chat_id, rol) VALUES (?, ?, ?, ?, ?)",
                (nombre, email, password_hash, chat_id, "usuario")
            )
            conn.commit()
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return jsonify({"error": "El email ya existe"}), 400
            return jsonify({"error": "Error desconocido", "detalle": str(e)}), 500
        finally:
            conn.close()

        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
