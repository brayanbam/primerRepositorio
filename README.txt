 Descripción del proyecto

TaskAPI es un sistema de gestión de tareas basado en una arquitectura de microservicios. Permite a los usuarios registrarse, iniciar sesión, consultar sus tareas y recibir notificaciones automáticas cuando tienen tareas pendientes.

El sistema está compuesto por cuatro servicios principales:

Servicio de Usuarios: gestión de usuarios, autenticación y generación de tokens JWT.
Servicio de Tareas: administración de tareas asociadas a usuarios.
Servicio de Notificaciones: envío de recordatorios de tareas pendientes mediante Telegram.
Frontend: interfaz web para interactuar con el sistema.

Cada servicio se ejecuta en un contenedor Docker, lo que permite un despliegue sencillo y portable.


INSTRUCCIONES PARA EJECUCIÓN

REQUISITOS
Tener instalado:
    - Docker
    - Docker Compose
    - Flask
    - Python
    - Node.js
    - Nginx


EJECUCIÓN DEL SISTEMA
Clonar el repositorio:
    - git clone https://github.com/brayanbam/primerRepositorio/tree/ronal
    - cd TaskAPI

Ejecutar los contenedores:
    - docker-compose up --build // docker-compose up -d 

Acceder al sistema:
Frontend:
    - http://localhost:8080

Servicios:
    - Usuarios: http://localhost:5001
    - Tareas: http://localhost:5002
    - Notificaciones: http://localhost:5003

Detener el sistema:
    - docker-compose down


AUTENTICACIÓN

El sistema utiliza JWT (JSON Web Tokens) para proteger los endpoints.

Para acceder a rutas protegidas debes incluir en los headers:
Authorization: Bearer TU_TOKEN

DESCRIPCIÓN BÁSICA DE ENDPOINTS

SERVICIO DE USUARIOS

Login:
    - POST /login
Autentica al usuario y retorna un token JWT.

Body:
{
  "email": "admin@gmail.com",
  "password": "1234567890"
}


Registro de usuario:
    - POST /usuarios
Permite crear un nuevo usuario.



Obtener usuarios (solo admin):
    - GET /usuarios



SERVICIO DE TAREAS

Obtener tareas:
    - GET /tareas

Admin: obtiene todas las tareas
Usuario: obtiene solo sus tareas

Crear tarea (solo admin):
    - POST /tareas

Completar tarea:
    - PUT /tareas/{id}/completar



SERVICIO DE NOTIFICACIONES

Este servicio funciona automáticamente:
    - Consulta tareas pendientes
    - Obtiene usuarios
    - Envía notificaciones mediante Telegram
(No requiere interacción directa desde el frontend)


Notas importantes
Se crea automáticamente un usuario administrador al iniciar el sistema:
Email: admin@gmail.com
Password: 1234567890

Solo el administrador puede crear tareas.
Los usuarios solo pueden ver y completar sus propias tareas.


 TECNOLOGIAS UTILICZADAS
Backend:
Python
Flask
Frontend:
Node.js
Nginx
Base de datos:
SQLite
Infraestructura:
Docker
Docker Compose


Arquitectura
El sistema sigue una arquitectura de microservicios, donde cada componente es independiente y se comunica mediante API REST.