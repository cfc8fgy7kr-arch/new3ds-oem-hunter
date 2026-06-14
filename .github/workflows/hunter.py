import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

mensaje = """🎮 New3DS OEM Hunter

✅ El bot está funcionando correctamente.

A partir de ahora podremos añadir búsquedas automáticas de pantallas OEM.
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": mensaje
    }
)

print("Mensaje enviado")
