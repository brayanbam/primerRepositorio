from flask import Flask, jsonify
import time

app = Flask(__name__)

print("Servicio [PEDIDOS] iniciado", flush=True)

@app.route("/pedidos")
def pedidos():

    print("Solicitud de [PEDIDOS] recibida", flush=True)

    inicio = time.time()

    respuesta = [
        {
            "id": 1,
            "producto": "Concentrado"
        }
    ]

    fin = time.time()
    tiempo_total = round(fin - inicio, 4)

    print(
        f"[PEDIDOS] respondió correctamente en {tiempo_total} segundos",
        flush=True
    )

    return jsonify(respuesta)


@app.route("/health")
def health():

    print("Health check en pedidos", flush=True)

    return {
        "servicio": "pedidos",
        "estado": "activo"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)