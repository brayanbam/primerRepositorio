# Pet Shop - Sistemas Distribuidos

Este proyecto implementa un sistema distribuido basado en microservicios, utilizando un API Gateway con el patrón **Circuit Breaker** para mejorar la resiliencia del sistema ante fallos.

---

## Problema

El sistema presentaba fallos cuando uno de los servicios dejaba de responder, ya que el gateway continuaba enviando solicitudes de forma repetitiva.  
Esto generaba:

- Sobrecarga del sistema  
- Aumento en los tiempos de respuesta  
- Riesgo de fallos en cascada  

---

## Solución

Se implementó el patrón **Circuit Breaker**, el cual:

- Detecta fallos repetidos  
- Detiene llamadas a servicios caídos  
- Permite la recuperación automática del sistema  

---

## Descripción del Sistema

El sistema está compuesto por tres microservicios:

- **Backend (Mascotas):** gestiona la información de mascotas  
- **Usuarios:** gestiona la información de usuarios  
- **Gateway:** punto de entrada que enruta las solicitudes  

El gateway es responsable de aplicar el patrón Circuit Breaker en cada endpoint.

---

## Arquitectura

Cliente → Gateway → Microservicios (Backend / Usuarios)

El gateway decide si enviar o bloquear una petición dependiendo del estado del circuito.

---

## Flujo de funcionamiento

1. El cliente realiza una petición al gateway  
2. El gateway verifica el estado del circuito  
3. Si el servicio está disponible → envía la solicitud  
4. Si hay fallos repetidos → abre el circuito  
5. Después de un tiempo → intenta recuperación automática  

---

##  Circuit Breaker Implementado

Cada endpoint (`/mascotas`, `/usuarios`, `/resumen`) maneja su propio circuito.

### Estados del circuito:

- **CLOSED:** funcionamiento normal  
- **OPEN:** se bloquean las peticiones  
- **HALF-OPEN:** se prueba la recuperación  

### Comportamiento:

- Después de 3 fallos → circuito se abre  
- Se espera un tiempo definido  
- Se realiza un nuevo intento  
        - Si funciona → se cierra  
        - Si falla → vuelve a abrir  

---

## Tecnologías Utilizadas

- Python 
- Flask  
- Docker 
- Docker Compose  

---

## Ejecución del Proyecto

1. Ubicarse en la raíz del proyecto

2. Ejecutar:

```bash
docker-compose up --build