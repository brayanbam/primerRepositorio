from flask import Flask
from flask_cors import CORS
from db import init_db
from routes import register_routes
from config import PORT

app = Flask(__name__)
CORS(app)

# Inicializa base de datos y rutas
init_db()
register_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=PORT)

