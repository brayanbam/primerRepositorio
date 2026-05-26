from flask import Flask
from flask_cors import CORS
from routes import register_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Registrar rutas
register_routes(app)


@app.route('/health')
def health():
    print("Health check en Analisis", flush=True)

    return {
        "servicio": "Analisis",
        "estado": "activo"
    }


    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
