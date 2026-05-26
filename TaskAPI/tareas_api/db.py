import sqlite3
from config import DATABASE

def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tareas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER,
                        titulo TEXT NOT NULL,
                        descripcion TEXT,
                        completada INTEGER DEFAULT 0,
                        intervalo_notificacion INTEGER DEFAULT 60
                    )''')
        conn.commit()
    finally:
        conn.close()
