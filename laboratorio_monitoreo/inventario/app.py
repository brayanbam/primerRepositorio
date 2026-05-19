from flask import Flask, jsonify
import time

app = Flask(__name__)

print("Servicio [INVENTARIO] iniciado", flush=True)

@app.route("/inventario")
def inventario():

    print("Consulta de [INVENTARIO] recibida", flush=True)

    inicio = time.time()

    respuesta = {
        "producto": "Concentrado",
        "stock": 10
    }

    fin = time.time()
    tiempo_total = round(fin - inicio, 4)

    print(
        f"[INVENTARIO] respondió correctamente en {tiempo_total} segundos",
        flush=True
    )

    return jsonify(respuesta)


@app.route("/health")
def health():

    print("Health check en inventario", flush=True)

    return {
        "servicio": "inventario",
        "estado": "activo"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)