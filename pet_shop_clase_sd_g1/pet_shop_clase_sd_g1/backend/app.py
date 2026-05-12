from flask import Flask, request, jsonify
import mysql.connector
import os
import requests
import time

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
       host = os.getenv("DB_HOST"),
       user = os.getenv("DB_USER"),
       password = os.getenv("DB_PASSWORD"),
       database = os.getenv("DB_NAME")
    )

@app.route("/relacion")
def relacion():
    usuarios = requests.get("http://usuarios:5000/usuarios").json()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT nombre FROM mascotas")
    mascotas = cursor.fetchall()  # Cambiado: traer todas
    connection.close()
    
    return {
        "usuarios": usuarios,
        "mascotas": [m[0] for m in mascotas]  # Lista de nombres
    }

@app.route("/")
def home():
    return "API FUNCIONANDO"

@app.route("/mascotas", methods=["POST"])
def crear_mascotas():
    data = request.json
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO mascotas (nombre, tipo, usuario_id) VALUES (%s, %s, %s)",
        (data["nombre"], data["tipo"], data.get("usuario_id", 1))  # Agregado usuario_id
    )
    connection.commit()
    connection.close()
    return {"mensaje": "mascota creada"}

@app.route("/mascotas", methods=["GET"])
def listar_mascotas():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, nombre, tipo, usuario_id FROM mascotas")
    mascotas = cursor.fetchall()
    connection.close()
    
    # Convertir a JSON con nombres de campos
    resultado = []
    for m in mascotas:
        resultado.append({
            "id": m[0],
            "nombre": m[1],
            "tipo": m[2],
            "usuario_id": m[3]
        })
    
    return jsonify(resultado)  # Usar jsonify

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)