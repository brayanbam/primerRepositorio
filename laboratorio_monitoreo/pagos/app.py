from flask import Flask, jsonify
import time

app = Flask(__name__)

print("Servicio [PAGOS] iniciado", flush=True)

@app.route("/pagos")
def pagos():

    print("Solicitud de [PAGOS] recibida", flush=True)

    inicio = time.time()

    respuesta = {
        "mensaje": "Pago realizado correctamente"
    }

    fin = time.time()
    tiempo_total = round(fin - inicio, 4)

    print(
        f"[PAGOS] respondió correctamente en {tiempo_total} segundos",
        flush=True
    )

    return jsonify(respuesta)


@app.route("/health")
def health():

    print("Health check en pagos", flush=True)

    return {
        "servicio": "pagos",
        "estado": "activo"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)