# Pet Shop - Sistemas Distribuidos

Este proyecto implementa un sistema distribuido basado en microservicios, utilizando un API Gateway con el patrón *Circuit Breaker* para mejorar la resiliencia del sistema ante fallos.

---

## Problema

El sistema presentaba fallos cuando uno de los servicios dejaba de responder, ya que el gateway continuaba enviando solicitudes de forma repetitiva.  
Esto generaba:

- Sobrecarga del sistema  
- Aumento en los tiempos de respuesta  
- Riesgo de fallos en cascada  

---

## Solución

Se implementó el patrón *Circuit Breaker*, el cual:

- Detecta fallos repetidos  
- Detiene llamadas a servicios caídos  
- Permite la recuperación automática del sistema  

---

## Descripción del Sistema

El sistema está compuesto por tres microservicios:

- *Backend (Mascotas):* gestiona la información de mascotas  
- *Usuarios:* gestiona la información de usuarios  
- *Gateway:* punto de entrada que enruta las solicitudes  

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

Cada endpoint (/mascotas, /usuarios, /resumen) maneja su propio circuito.

### Estados del circuito:

- *CLOSED:* funcionamiento normal  
- *OPEN:* se bloquean las peticiones  
- *HALF-OPEN:* se prueba la recuperación  

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
Cortacircuitos
¿Qué es?

El patrón Circuit Breaker es un mecanismo de resiliencia utilizado en arquitecturas de microservicios.

Su objetivo es evitar solicitudes repetitivas hacia servicios que están fallando, evitando la sobrecarga del sistema y tiempos de espera innecesarios.

FASE 1 – OBSERVADOR
¿Qué hace el sistema actualmente?
Inicialmente, el sistema intenta conectarse al servicio backend cada vez que se realiza una solicitud al endpoint /mascotas.

Cuando el servicio falla, el gateway detecta el error y aumenta un contador de fallos. Después de varios intentos fallidos, el circuito se abre y el sistema deja de intentar conexiones al servicio caído.

¿Se protege o insiste?
El sistema primero insiste en realizar las conexiones mientras el número de fallos sea menor al límite configurado.

Después de alcanzar el límite de fallos, el sistema se protege abriendo el circuito y bloqueando temporalmente nuevas solicitudes hacia el servicio que presenta errores.

Estados del Circuit Breaker
1. CERRADO
El servicio funciona normalmente y las solicitudes se procesan sin restricciones.

2. ABRIR
Después de varios fallos consecutivos, el circuito se abre.

El gateway deja de intentar conexiones al servicio caído.

Esto evita:

sobrecarga
tiempos de espera innecesarios
consumo excesivo de recursos
3. SEMIABIERTO
Después de un tiempo de espera, el sistema permite realizar una nueva solicitud de prueba al servicio.

Si funciona:
el circuito se cierra
el servicio vuelve a operar normalmente
Si falla:
el circuito vuelve a abrirse
se reinicia el tiempo de espera
FASE 2 – APLICADOR
Implementación Realizada
El patrón Circuit Breaker fue implementado en el gateway para los siguientes puntos finales:

/usuarios
/mascotas
/relacion
¿Cada servicio debe tener su propio contador de fallos?
Si. Cada servicio debe tener su propio contador de fallos porque los microservicios funcionan de manera independiente.

Esto permite detectar errores específicos de cada servicio sin afectar a los demás.

¿El circuito debe abrirse de forma independiente por servicio?
Si. Cada servicio posee su propio circuito independiente.

De esta manera, si un servicio falla, únicamente se bloquearán las solicitudes hacia ese servicio específico.

¿Qué pasa si falla un servicio pero el otro sigue funcionando?
Los demás servicios continúan funcionando normalmente.

Por ejemplo, si el backend falla, el endpoint /mascotaspuede bloquearse temporalmente, mientras /usuarioscontinúa respondiendo correctamente.

Esto mejora la disponibilidad general del sistema.

Lógica Implementada
Configuración
LIMITE_FALLOS = 3
TIEMPO_RECUPERACION = 10
LIMITE_FALLOS: cantidad máxima de errores permitidos antes de abrir el circuito.
TIEMPO_RECUPERACION: tiempo de espera antes de intentar una nueva conexión.
FASE 3 – INVESTIGAR (Medioabierto)
¿Qué significa “medio abierto”?
Half-Open es un estado intermedio del Circuit Breaker.

Después de permanecer abierto durante un tiempo determinado, el sistema permite una nueva solicitud de prueba para verificar si el servicio ya se recuperó.

¿Cuándo se vuelve a intentar una llamada?
La llamada se vuelve a intentar después de que finalice el tiempo de recuperación configurado.

¿Qué pasa si el servicio vuelve a fallar?
Si la nueva solicitud falla nuevamente:

el circuito vuelve al estado OPEN
se reinicia el tiempo de espera
se bloquearán nuevamente las solicitudes
FASE 5 – VALIDAR
1. Servicio funcionando
El gateway responde normalmente a las solicitudes.

Ejemplo:

{
    "mascotas":[[1,"Firulais","Perro"]]
}
2. Servicio caído
Al detener el servicio backend:

docker compose stop backend
El gateway detecta el fallo y responde:

{
  "error": "Servicio backend no disponible"
}
3. Circuito abierto
Después de múltiples fallos consecutivos:

{
  "error": "Circuito abierto para backend"
}
El sistema deja de intentar conexiones temporalmente.

4. Recuperación del servicio
Después de reiniciar el servicio:

docker compose start backend
El sistema espera el tiempo configurado y realiza una nueva prueba de conexión.

Si la conexión funciona correctamente:

Intentando reconectar con backend
backend funcionando correctamente
El circuito vuelve al estado CERRADO y las solicitudes se procesan normalmente.

Análisis final
¿Qué cambió en el comportamiento del sistema?

Inicialmente, el sistema intentaba conectarse continuamente a los servicios aunque estuvieran caídos, generando múltiples errores y solicitudes innecesarias.

Después de implementar el patrón Circuit Breaker en todos los endpoints del gateway, el sistema ahora puede detectar fallos repetitivos y bloquear temporalmente las conexiones hacia los servicios afectados.

Además, con la implementación del estado Half-Open, el sistema puede intentar recuperarse automáticamente cuando el servicio vuelve a estar disponible.

Esto mejoró la estabilidad, resiliencia y control de errores dentro de la arquitectura de microservicios.

¿Qué decisiones tomaron en la implementación?

Se decidió implementar el Circuit Breaker en el gateway porque es el componente encargado de consumir y redirigir solicitudes hacia los microservicios.

También se decidió:

utilizar un contador de fallos independiente por servicio manejar circuitos independientes para cada endpoint implementar un tiempo de recuperación configurable agregar el estado Half-Open para permitir recuperación automática reutilizar la lógica mediante una función general para evitar duplicar código

Estas decisiones permitieron que un servicio pudiera fallar sin afectar el funcionamiento de los demás.

¿Qué dificultades encontraron?

Durante la implementación se encontraron varias dificultades:

comprender correctamente el funcionamiento de los estados CERRADO, ABIERTO y MEDIO ABIERTO controlar el tiempo de recuperación usando time manejar correctamente los errores de conexión con solicitudes evitar duplicar código entre endpoints probar la recuperación automática de los servicios entender cómo Docker maneja la comunicación entre contenedores

También fue necesario analizar cómo aplicar el Disyuntor de manera independiente para cada servicio sin afectar el comportamiento global del sistema.
