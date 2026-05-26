from flask import Flask
from flask_cors import CORS
from scheduler import programar_notificaciones
from config import PORT
import threading
import time

app = Flask(__name__)
CORS(app)

scheduler_iniciado = False

def iniciar_scheduler():
    global scheduler_iniciado
    if not scheduler_iniciado:
        time.sleep(3)  # esperar a que APIs estén arriba
        programar_notificaciones()
        scheduler_iniciado = True
        print("🕒 Scheduler iniciado correctamente (una sola instancia).")

@app.route('/')
def home():
    return "Servidor de notificaciones activo ✅", 200


@app.route("/health")
def health():

    print("Health check en Notificaciones", flush=True)

    return {
        "servicio": "Notificaciones",
        "estado": "activo"
    }


if __name__ == '__main__':
    print("🚀 Servidor de notificaciones iniciado...")
    hilo = threading.Thread(target=iniciar_scheduler)
    hilo.start()
    app.run(host="0.0.0.0", debug=True, port=5000, use_reloader=False)

