import requests
from config import TELEGRAM_TOKEN

def enviar_mensaje(chat_id, texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto}
    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f" Error enviando mensaje a {chat_id}: {e}")
