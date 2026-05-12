from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

TIEMPO_ESPERA = 10

#  MASCOTAS
fallos_backend = 0
estado_mascotas = "CLOSED"
tiempo_mascotas = 0 #cuándo falló por última vez

# USUARIOS
fallos_usuarios = 0
estado_usuarios = "CLOSED"
tiempo_usuarios = 0

# RESUMEN
fallos_resumen = 0
estado_resumen = "CLOSED"
tiempo_resumen = 0


@app.route("/mascotas")
def mascotas():
    global fallos_backend, estado_mascotas, tiempo_mascotas

    if estado_mascotas == "OPEN":
        if time.time() - tiempo_mascotas > TIEMPO_ESPERA:
            estado_mascotas = "HALF-OPEN"
            print("Mascotas en HALF-OPEN", flush=True)
        else:
            return {"error": "Servicio mascotas bloqueado"}, 503

    try:
        response = requests.get("http://backend:5000/mascotas", timeout=2)

        # Si funciona
        estado_mascotas = "CLOSED"
        fallos_backend = 0

        return jsonify(response.json())

    except:
        tiempo_mascotas = time.time()

        if estado_mascotas == "HALF-OPEN":
            estado_mascotas = "OPEN"
            print("Mascotas vuelve a OPEN", flush=True)
        else:
            fallos_backend += 1
            print(f"Fallo mascotas #{fallos_backend}", flush=True)

            if fallos_backend >= 3:
                estado_mascotas = "OPEN"
                print("Circuito mascotas OPEN", flush=True)

        return {"error": "Servicio mascotas no disponible"}, 503


@app.route("/usuarios")
def usuarios():
    global fallos_usuarios, estado_usuarios, tiempo_usuarios

    if estado_usuarios == "OPEN":
        if time.time() - tiempo_usuarios > TIEMPO_ESPERA:
            estado_usuarios = "HALF-OPEN"
            print("Usuarios en HALF-OPEN", flush=True)
        else:
            return {"error": "Servicio usuarios bloqueado"}, 503

    try:
        response = requests.get("http://usuarios:5000/usuarios", timeout=2)

        estado_usuarios = "CLOSED"
        fallos_usuarios = 0

        return jsonify(response.json())

    except:
        tiempo_usuarios = time.time()

        if estado_usuarios == "HALF-OPEN":
            estado_usuarios = "OPEN"
            print("Usuarios vuelve a OPEN", flush=True)
        else:
            fallos_usuarios += 1
            print(f"Fallo usuarios #{fallos_usuarios}", flush=True)

            if fallos_usuarios >= 3:
                estado_usuarios = "OPEN"

        return {"error": "Servicio usuarios no disponible"}, 503


@app.route("/resumen")
def resumen():
    global fallos_resumen, estado_resumen, tiempo_resumen

    if estado_resumen == "OPEN":
        if time.time() - tiempo_resumen > TIEMPO_ESPERA:
            estado_resumen = "HALF-OPEN"
            print("Resumen en HALF-OPEN", flush=True)
        else:
            return {"error": "Servicio resumen bloqueado"}, 503

    try:
        response = requests.get("http://backend:5000/resumen", timeout=2)

        estado_resumen = "CLOSED"
        fallos_resumen = 0

        return jsonify(response.json())

    except:
        tiempo_resumen = time.time()

        if estado_resumen == "HALF-OPEN":
            estado_resumen = "OPEN"
            print("Resumen vuelve a OPEN", flush=True)
        else:
            fallos_resumen += 1
            print(f"Fallo resumen #{fallos_resumen}", flush=True)

            if fallos_resumen >= 3:
                estado_resumen = "OPEN"

        return {"error": "Servicio resumen no disponible"}, 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)