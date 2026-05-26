TaskAPI - Sistemas Distribuidos

Este proyecto implementa un sistema distribuido basado en microservicios para la gestión de tareas personales y laborales, incluyendo autenticación, notificaciones automáticas y análisis de productividad.

Problema

En la actualidad, muchas personas gestionan sus tareas de forma manual o mediante aplicaciones básicas que no ofrecen análisis ni notificaciones inteligentes.

Esto genera problemas como:

Olvido de tareas importantes
Falta de seguimiento de productividad
Poca visibilidad del progreso personal o laboral
Solución

Se desarrolló TaskAPI, un sistema basado en microservicios que permite:

Gestión de usuarios y autenticación segura
Creación y administración de tareas
Notificaciones automáticas mediante Telegram
Generación de métricas y análisis del sistema
Control de acceso basado en roles (admin / usuario)
Descripción del Sistema

El sistema está compuesto por los siguientes microservicios:

Servicio de Usuarios: registro, login y gestión de roles con JWT
Servicio de Tareas: creación, consulta y actualización de tareas
Servicio de Notificaciones: envío de recordatorios por Telegram
Servicio de Análisis: generación de métricas, dashboard y productividad
Frontend: interfaz de usuario para interactuar con el sistema
API Gateway (si aplica): punto central de comunicación entre servicios
Arquitectura

Cliente → Frontend → Gateway → Microservicios

Los microservicios se comunican mediante solicitudes HTTP REST dentro de una red interna gestionada por Docker Compose.

Además:

El frontend consume los servicios de usuarios y tareas
El servicio de notificaciones consulta tareas y usuarios
El servicio de análisis consume datos del servicio de tareas para generar métricas
Flujo de funcionamiento
El usuario accede al sistema desde el frontend
Se autentica mediante el servicio de usuarios (JWT)
El frontend consume los servicios de tareas
El servicio de notificaciones envía alertas a usuarios con tareas pendientes
El servicio de análisis procesa datos del sistema y genera estadísticas
Funcionalidades del Sistema
Registro de usuarios
Inicio de sesión con JWT
Gestión de roles (admin / usuario)
Creación y gestión de tareas
Marcado de tareas como completadas
Notificaciones automáticas por Telegram
Dashboard administrativo
Análisis de productividad por usuario
Estadísticas generales del sistema
Comunicación entre microservicios vía API REST
Servicio de Análisis

El servicio de análisis es responsable de:

Generar métricas generales del sistema
Calcular productividad por usuario
Obtener tareas completadas y pendientes
Proveer un dashboard administrativo

Endpoints principales:

/dashboard → métricas generales
/productividad → productividad por usuario
/completadas → tareas completadas
/estadisticas → resumen del sistema
Tecnologías Utilizadas
Python
Flask
Node.js (Frontend)
Nginx
Docker
Docker Compose
SQLite
JWT (Autenticación)
Telegram Bot API
Contenerización

Cada microservicio se ejecuta en un contenedor independiente, lo que permite:

Aislamiento de servicios
Escalabilidad
Facilidad de despliegue
Comunicación interna mediante red Docker
Ejecución del Proyecto
Clonar el repositorio
Ubicarse en la raíz del proyecto
Ejecutar el sistema con Docker Compose:
docker-compose up --build
Resultado

El sistema permite gestionar tareas de forma eficiente, recibir notificaciones automáticas y visualizar métricas de productividad en tiempo real, todo bajo una arquitectura de microservicios distribuida.
