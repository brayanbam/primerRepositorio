# analytics_api/routes.py
from flask import jsonify, request
from datetime import datetime, timedelta
import requests
import jwt
from functools import wraps
from config import Config

# Datos mock para pruebas
MOCK_TAREAS = [
    {"id": 1, "usuario_id": 1, "titulo": "Tarea 1", "estado": "completada", "fecha_creacion": "2026-05-15", "fecha_completada": "2026-05-16"},
    {"id": 2, "usuario_id": 1, "titulo": "Tarea 2", "estado": "completada", "fecha_creacion": "2026-05-14", "fecha_completada": "2026-05-15"},
    {"id": 3, "usuario_id": 1, "titulo": "Tarea 3", "estado": "pendiente", "fecha_creacion": "2026-05-13", "fecha_completada": None},
    {"id": 4, "usuario_id": 2, "titulo": "Tarea 4", "estado": "completada", "fecha_creacion": "2026-05-12", "fecha_completada": "2026-05-14"},
    {"id": 5, "usuario_id": 1, "titulo": "Tarea 5", "estado": "completada", "fecha_creacion": "2026-05-10", "fecha_completada": "2026-05-11"},
]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({"error": "Token inválido"}), 401
        
        return f(*args, **kwargs)
    return decorated

def register_routes(app):
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email y password requeridos"}), 400
        
        if data['email'] == Config.ADMIN_EMAIL and data['password'] == Config.ADMIN_PASSWORD:
            token = jwt.encode({
                'user_id': 1,
                'email': data['email'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, Config.SECRET_KEY, algorithm='HS256')
            
            return jsonify({"token": token, "message": "Login exitoso"})
        
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        tareas = MOCK_TAREAS
        
        total_tareas = len(tareas)
        tareas_completadas = len([t for t in tareas if t.get('estado') == 'completada'])
        tareas_pendientes = total_tareas - tareas_completadas
        porcentaje = (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0
        
        return jsonify({
            "metricas_generales": {
                "total_tareas": total_tareas,
                "tareas_completadas": tareas_completadas,
                "tareas_pendientes": tareas_pendientes,
                "porcentaje_completado": round(porcentaje, 2)
            },
            "fecha_consulta": datetime.now().isoformat()
        })
    
    @app.route('/productividad/usuarios', methods=['GET'])
    def productividad_usuarios():
        tareas = MOCK_TAREAS
        usuarios = [{"id": 1, "nombre": "Usuario 1"}, {"id": 2, "nombre": "Usuario 2"}]
        
        productividad = {}
        for usuario in usuarios:
            tareas_usuario = [t for t in tareas if t.get('usuario_id') == usuario['id']]
            completadas = len([t for t in tareas_usuario if t.get('estado') == 'completada'])
            total = len(tareas_usuario)
            productividad[usuario['nombre']] = {
                "tareas_completadas": completadas,
                "tareas_totales": total,
                "porcentaje": round((completadas / total * 100) if total > 0 else 0, 2)
            }
        
        return jsonify({"productividad_por_usuario": productividad})
    
    @app.route('/tiempo/promedio', methods=['GET'])
    def tiempo_promedio():
        tareas = MOCK_TAREAS
        tareas_completadas = [t for t in tareas if t.get('estado') == 'completada' 
                              and t.get('fecha_creacion') and t.get('fecha_completada')]
        
        tiempos = []
        for tarea in tareas_completadas:
            fecha_creacion = datetime.strptime(tarea['fecha_creacion'], '%Y-%m-%d')
            fecha_completada = datetime.strptime(tarea['fecha_completada'], '%Y-%m-%d')
            dias = (fecha_completada - fecha_creacion).days
            tiempos.append(dias)
        
        promedio = sum(tiempos) / len(tiempos) if tiempos else 0
        
        return jsonify({
            "tiempo_promedio_completado": {
                "dias": round(promedio, 1),
                "horas": round(promedio * 24, 1),
                "total_tareas_analizadas": len(tiempos)
            }
        })
    
    @app.route('/metricas/diarias', methods=['GET'])
    def metricas_diarias():
        tareas = MOCK_TAREAS
        tareas_completadas = [t for t in tareas if t.get('estado') == 'completada' and t.get('fecha_completada')]
        
        metricas = {}
        for i in range(7):
            fecha = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            metricas[fecha] = 0
        
        for tarea in tareas_completadas:
            fecha_completada = tarea.get('fecha_completada')
            if fecha_completada in metricas:
                metricas[fecha_completada] += 1
        
        return jsonify({
            "tareas_completadas_por_dia": metricas,
            "periodo": "últimos 7 días"
        })