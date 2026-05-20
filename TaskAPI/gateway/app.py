from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

print("🚀 Gateway iniciado correctamente", flush=True)

# --------------------------------
# MÉTRICAS
# --------------------------------
errores = {
    "usuarios": 0,
    "tareas": 0,
    "notificaciones": 0
}

tiempos_respuesta = {
    "usuarios": 0,
    "tareas": 0,
    "notificaciones": 0
}

# --------------------------------
# CIRCUIT BREAKER
# --------------------------------
servicios = {
    "usuarios": {
        "fallos": 0,
        "abierto": False,
        "ultimo_fallo": 0
    },
    "tareas": {
        "fallos": 0,
        "abierto": False,
        "ultimo_fallo": 0
    },
    "notificaciones": {
        "fallos": 0,
        "abierto": False,
        "ultimo_fallo": 0
    }
}

LIMITE_FALLOS = 3
TIEMPO_RECUPERACION = 10


# --------------------------------
# FUNCIÓN GENERAL
# --------------------------------
def consultar_servicio(
    nombre,
    metodo,
    url,
    headers=None,
    data=None
):

    servicio = servicios[nombre]

    print(f"\n[GATEWAY] Consultando servicio: {nombre}", flush=True)

    # --------------------------------
    # VERIFICAR CIRCUITO
    # --------------------------------
    if servicio["abierto"]:

        tiempo_actual = time.time()

        tiempo_espera = (
            tiempo_actual - servicio["ultimo_fallo"]
        )

        # HALF OPEN
        if tiempo_espera >= TIEMPO_RECUPERACION:

            print(
                f"🔄 Intentando reconectar con {nombre}",
                flush=True
            )

        else:

            print(
                f"⛔ Circuito abierto para {nombre}",
                flush=True
            )

            return jsonify({
                "error": f"Circuito abierto para {nombre}"
            }), 503

    inicio = time.time()

    try:

        # --------------------------------
        # REQUEST
        # --------------------------------
        if metodo == "GET":

            response = requests.get(
                url,
                headers=headers,
                timeout=5
            )

        elif metodo == "POST":

            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=5
            )

        fin = time.time()

        tiempo_total = round(fin - inicio, 4)

        tiempos_respuesta[nombre] = tiempo_total

        # --------------------------------
        # RESETEAR CIRCUIT BREAKER
        # --------------------------------
        servicio["fallos"] = 0
        servicio["abierto"] = False

        print(
            f"✅ {nombre} respondió correctamente en {tiempo_total} segundos",
            flush=True
        )

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:

        # --------------------------------
        # MANEJO DE ERRORES
        # --------------------------------
        errores[nombre] += 1

        servicio["fallos"] += 1

        print(
            f"❌ ERROR conectando con {nombre}",
            flush=True
        )

        print(
            f"Cantidad de errores: {errores[nombre]}",
            flush=True
        )

        print(
            f"Fallos consecutivos: {servicio['fallos']}",
            flush=True
        )

        print(
            f"Detalle: {str(e)}",
            flush=True
        )

        # --------------------------------
        # ABRIR CIRCUITO
        # --------------------------------
        if servicio["fallos"] >= LIMITE_FALLOS:

            servicio["abierto"] = True

            servicio["ultimo_fallo"] = time.time()

            print(
                f"⛔ Circuito abierto para {nombre}",
                flush=True
            )

        return jsonify({
            "error": f"Servicio {nombre} no disponible"
        }), 503


# --------------------------------
# LOGIN
# --------------------------------
@app.route('/login', methods=['POST'])
def login():

    print("📥 Solicitud recibida en /login", flush=True)

    return consultar_servicio(
        "usuarios",
        "POST",
        "http://usuarios:5000/login",
        data=request.json
    )


# --------------------------------
# USUARIOS
# --------------------------------
@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():

    print(
        f"📥 Solicitud recibida en /usuarios [{request.method}]",
        flush=True
    )

    headers = {
        "Authorization": request.headers.get("Authorization", "")
    }

    if request.method == 'GET':

        return consultar_servicio(
            "usuarios",
            "GET",
            "http://usuarios:5000/usuarios",
            headers=headers
        )

    return consultar_servicio(
        "usuarios",
        "POST",
        "http://usuarios:5000/usuarios",
        data=request.json
    )


# --------------------------------
# TAREAS
# --------------------------------
@app.route('/tareas', methods=['GET', 'POST'])
def tareas():

    print(
        f"📥 Solicitud recibida en /tareas [{request.method}]",
        flush=True
    )

    headers = {
        "Authorization": request.headers.get("Authorization", "")
    }

    if request.method == 'GET':

        return consultar_servicio(
            "tareas",
            "GET",
            "http://tareas:5000/tareas",
            headers=headers
        )

    return consultar_servicio(
        "tareas",
        "POST",
        "http://tareas:5000/tareas",
        headers=headers,
        data=request.json
    )


# --------------------------------
# MONITOR
# --------------------------------
@app.route('/monitor')
def monitor():

    print("\n📊 Ejecutando monitoreo general", flush=True)

    estados = {}

    for nombre, datos in servicios.items():

        if datos["abierto"]:

            estados[nombre] = "circuito_abierto"

        else:

            estados[nombre] = "activo"

    return jsonify(estados)


# --------------------------------
# MÉTRICAS
# --------------------------------
@app.route('/metricas')
def metricas():

    print("\n📈 Consultando métricas", flush=True)

    return jsonify({
        "errores": errores,
        "tiempos_respuesta": tiempos_respuesta,
        "circuit_breaker": servicios
    })


# --------------------------------
# MAIN
# --------------------------------
if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000
    )