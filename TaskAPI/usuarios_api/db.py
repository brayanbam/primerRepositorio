import sqlite3
from config import DATABASE
from werkzeug.security import generate_password_hash

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
        c.execute("SELECT * FROM usuarios WHERE email = ?", ("admin@gmail.com",))
        if not c.fetchone():
            password = generate_password_hash("1234567890", method='pbkdf2:sha256')
            c.execute("""
                INSERT INTO usuarios (nombre, email, password, rol)
                VALUES (?, ?, ?, ?)
            """, ("ADMIN", "admin@gmail.com", password, "admin"))
            print("✔ Usuario administrador creado")

        conn.commit()
    finally:
        conn.close()
