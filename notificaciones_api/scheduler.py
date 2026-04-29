from apscheduler.schedulers.background import BackgroundScheduler
import requests
from telegram_utils import enviar_mensaje
from config import USUARIOS_API, TAREAS_API, NOTIFICACIONES_TOKEN

scheduler = BackgroundScheduler()

def verificar_y_enviar_notificaciones():
    headers = {"Authorization": f"Bearer {NOTIFICACIONES_TOKEN}"}

    try:
        # Obtener usuarios
        resp_usuarios = requests.get(USUARIOS_API, headers=headers, timeout=5)
        resp_usuarios.raise_for_status()
        data_usuarios = resp_usuarios.json()
        usuarios = data_usuarios.get("usuarios", []) if isinstance(data_usuarios, dict) else []

        # Obtener tareas
        resp_tareas = requests.get(TAREAS_API, headers=headers, timeout=5)
        resp_tareas.raise_for_status()
        data_tareas = resp_tareas.json()
        tareas = data_tareas.get("tareas", []) if isinstance(data_tareas, dict) else []

    except requests.RequestException as e:
        print("❌ Error al obtener datos de la API:", e)
        return
    except ValueError as e:
        print("❌ Error al decodificar JSON:", e)
        return

    for usuario in usuarios:
        chat_id = usuario.get('chat_id')
        if not chat_id:
            continue
        for tarea in tareas:
            if tarea.get('usuario_id') == usuario.get('id') and not tarea.get('completada', False):
                mensaje = f"📋 *Tarea pendiente:* {tarea.get('titulo')}\n📝 {tarea.get('descripcion','')}"
                enviar_mensaje(chat_id, mensaje)
                print(f"✅ Notificación enviada al usuario {usuario.get('id')} - {tarea.get('titulo')}")

def programar_notificaciones():
    if not scheduler.get_job('notificador_global'):
        scheduler.add_job(
            verificar_y_enviar_notificaciones,
            trigger='interval',
            minutes=1,
            id='notificador_global',
            replace_existing=True
        )
        scheduler.start()
        print("🕒 Scheduler activo y programado para cada minuto.")
