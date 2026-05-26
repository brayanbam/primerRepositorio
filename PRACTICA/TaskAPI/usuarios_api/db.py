import sqlite3
from config import DATABASE
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_connection()
    try:
        c = conn.cursor()
        
        # Crear tabla de usuarios si no existe
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        chat_id TEXT,
                        rol TEXT DEFAULT 'usuario'
                    )''')

        # Crear administrador si no existe
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        c.execute("SELECT * FROM usuarios WHERE email = ?", (admin_email,))
        if not c.fetchone():
            password = generate_password_hash(admin_password, method='pbkdf2:sha256')
            c.execute("""
                INSERT INTO usuarios (nombre, email, password, rol)
                VALUES (?, ?, ?, ?)
            """, ("ADMIN", admin_email, password, "admin"))
            print("✔ Usuario administrador creado")

        conn.commit()
    finally:
        conn.close()
