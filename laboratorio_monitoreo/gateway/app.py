from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

print("Gateway iniciado correctamente", flush=True)

errores = {
    "pedidos": 0,
    "inventario": 0,
    "pagos": 0
}

tiempos_respuesta = {
    "pedidos": 0,
    "inventario": 0,
    "pagos": 0
}


def consultar_servicio(nombre, url):

    print(f"[GATEWAY] Consultando servicio {nombre}", flush=True)

    inicio = time.time()

    try:

        response = requests.get(url, timeout=3)

        fin = time.time()

        tiempo_total = round(fin - inicio, 4)

        tiempos_respuesta[nombre] = tiempo_total

        print(
            f"{nombre} respondió correctamente en {tiempo_total} segundos",
            flush=True
        )

        return jsonify(response.json())

    except requests.exceptions.RequestException:

        errores[nombre] += 1

        print(
            f"ERROR conectando con {nombre}",
            flush=True
        )

        print(
            f"Cantidad de errores en {nombre}: {errores[nombre]}",
            flush=True
        )

        return {
            "error": f"Servicio {nombre} no disponible"
        }, 503





@app.route("/pedidos")
def pedidos():

    print("Solicitud recibida en endpoint /pedidos", flush=True)

    return consultar_servicio(
        "pedidos",
        "http://pedidos:5000/pedidos"
    )


@app.route("/inventario")
def inventario():

    print("Solicitud recibida en endpoint /inventario", flush=True)

    return consultar_servicio(
        "inventario",
        "http://inventario:5000/inventario"
    )


@app.route("/pagos")
def pagos():

    print("Solicitud recibida en endpoint /pagos", flush=True)

    return consultar_servicio(
        "pagos",
        "http://pagos:5000/pagos"
    )





@app.route("/monitor")
def monitor():

    print("Ejecutando monitoreo general", flush=True)

    servicios = {
        "pedidos": "http://pedidos:5000/health",
        "inventario": "http://inventario:5000/health",
        "pagos": "http://pagos:5000/health"
    }

    estados = {}

    for nombre, url in servicios.items():

        try:

            requests.get(url, timeout=2)

            estados[nombre] = "activo"

            print(f"{nombre} ACTIVO", flush=True)

        except:

            estados[nombre] = "caido"

            print(f"{nombre} CAIDO", flush=True)

    return jsonify(estados)






@app.route("/metricas")
def metricas():

    print("Consultando métricas del sistema", flush=True)

    return jsonify({
        "errores": errores,
        "tiempos_respuesta": tiempos_respuesta
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)