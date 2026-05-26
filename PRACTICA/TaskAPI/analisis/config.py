import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'

    # URLs de otros servicios
    TAREAS_API_URL = os.getenv(
        'TAREAS_API_URL',
        'http://tareas_api:5000'
    )

    USUARIOS_API_URL = os.getenv(
        'USUARIOS_API_URL',
        'http://usuarios_api:5000'
    )