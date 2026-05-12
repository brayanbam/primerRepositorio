from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

MAX_FALLOS = 3
TIEMPO_ESPERA = 10

fallos_mascotas = 0
circuito_mascotas = False
ultimo_fallo_mascotas = 0

fallos_usuarios = 0
circuito_usuarios = False
ultimo_fallo_usuarios = 0

@app.route("/usuarios")
def usuarios():

    global fallos_usuarios
    global circuito_usuarios
    global ultimo_fallo_usuarios

    # si el circuito esta abierto
    if circuito_usuarios:

        tiempo_pasado = time.time() - ultimo_fallo_usuarios

        # revisa si ya puede intentar otra vez
        if tiempo_pasado > TIEMPO_ESPERA:
            print("Intentando recuperar servicio usuarios...", flush=True)

        else:
            return jsonify({
                "error": "Servicio usuarios bloqueado temporalmente"}), 503

    try:
        response = requests.get("http://usuarios:5000/usuarios",timeout=2)
        # si funciona se reinicia todo
        fallos_usuarios = 0
        circuito_usuarios = False

        print("Servicio usuarios recuperado", flush=True)

        return jsonify(response.json())

    except:

        fallos_usuarios += 1

        print(f"Fallo usuarios: {fallos_usuarios}", flush=True)

        # guarda el momento del fallo
        ultimo_fallo_usuarios = time.time()

        if fallos_usuarios >= MAX_FALLOS:
            circuito_usuarios = True
            print("Circuito usuarios abierto", flush=True)

        return jsonify({
            "error": "Servicio usuarios no disponible"}), 503
    
@app.route("/mascotas")
def mascotas():
    global fallos_mascotas
    global circuito_mascotas
    global ultimo_fallo_mascotas

    if circuito_mascotas:

        tiempo_pasado = time.time() - ultimo_fallo_mascotas

        if tiempo_pasado > TIEMPO_ESPERA:
            print("Intentando recuperar servicio mascotas...", flush=True)

        else:
            return jsonify({
                "error": "Servicio mascotas bloqueado temporalmente"}), 503

    try:
        response = requests.get(
            "http://backend:5000/mascotas",timeout=2)
        
        fallos_mascotas = 0
        circuito_mascotas = False

        print("Servicio mascotas recuperado", flush=True)

        return jsonify(response.json())

    except:

        fallos_mascotas += 1

        print(f"Fallo mascotas: {fallos_mascotas}", flush=True)

        ultimo_fallo_mascotas = time.time()

        if fallos_mascotas >= MAX_FALLOS:
            circuito_mascotas = True
            print("Circuito mascotas abierto", flush=True)

        return jsonify({
            "error": "Servicio mascotas no disponible"
        }), 503

@app.route("/resumen")
def resumen():
    resultado = {}
    try:
        r = requests.get(
            "http://backend:5000/mascotas",timeout=2)

        resultado["mascotas"] = r.json()

    except:
        resultado["mascotas"] = {
            "error": "Servicio mascotas no disponible"
        }
    try:
        r = requests.get(
            "http://usuarios:5000/usuarios",timeout=2)

        resultado["usuarios"] = r.json()

    except:
        resultado["usuarios"] = {"error": "Servicio usuarios no disponible"}

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)