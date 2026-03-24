📌 TaskAPI - Sistema de Gestión de Tareas con Notificaciones
🧠 Descripción

TaskAPI es un sistema basado en microservicios que permite la gestión de usuarios y tareas, incluyendo un módulo de notificaciones automáticas.

El sistema está desarrollado con Flask (backend), Vue (frontend) y desplegado mediante Docker Compose, permitiendo una arquitectura modular y escalable.

- 🐍 Python 3.10 (lenguaje principal para el desarrollo del backend)
- 🔥 Flask (framework web ligero para la construcción de APIs)
- 🌐 Flask-CORS (gestión de políticas CORS para permitir comunicación entre frontend y backend)
- 🔐 PyJWT (implementación de autenticación basada en tokens JWT)
- 🗄️ SQLite (base de datos ligera utilizada para almacenamiento local)
- 🐳 Docker (contenedorización de los servicios)
- 📦 Docker Compose (orquestación de múltiples contenedores)
- 🧩 Arquitectura de microservicios (separación del sistema en servicios independientes)
- ⚡ Vue.js (framework JavaScript para la construcción del frontend)
- 🟢 Node.js (entorno de ejecución usado para construir y gestionar el frontend)
- 🌍 Nginx (servidor web utilizado para servir el frontend)



🏗️ Arquitectura del sistema

El sistema está compuesto por 4 servicios principales:
usuarios → Gestión de usuarios y autenticación
tareas → Gestión de tareas
notificaciones → Envío automático de alertas
frontend → Interfaz de usuario (Vue + Nginx)



🚀 Cómo ejecutar el proyecto
1. Clonar el repositorio
git clone <TU_REPOSITORIO>
cd TaskAPI
2. Ejecutar con Docker
docker-compose up --build
3. Acceder al sistema
Frontend: http://localhost:8080



👤 Roles de usuario
admin → acceso completo
usuario → acceso limitado



🔔 Sistema de notificaciones

El microservicio de notificaciones:
Consulta tareas pendientes
Consulta usuarios
Envía alertas automáticamente (ej: Telegram)



🔗 Comunicación entre servicios

Dentro de Docker:
usuarios → http://usuarios:5001
tareas → http://tareas:5002