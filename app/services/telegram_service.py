import requests
import os
from flask import current_app, request, jsonify
from app.config.telegram import TELEGRAM_BOT_TOKEN, WEBHOOK_ENDPOINT
from app.services.user_service import update_user_chat_id

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def set_webhook():
    """Set Telegram webhook ke endpoint VPS."""
    url = f"{API_URL}/setWebhook"
    response = requests.post(url, data={"url": WEBHOOK_ENDPOINT})

    if response.status_code == 200 and response.json().get("ok"):
        return True
    else:
        current_app.logger.error(f"Gagal set webhook: {response.text}")
        return False


def send_message(chat_id, text):
    """Kirim pesan ke chat_id tertentu."""
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        current_app.logger.error(f"Gagal mengirim pesan ke Telegram: {response.text}")
        return False
    return True


def handle_message(data):
    """Proses pesan masuk dari webhook Telegram."""
    if "message" not in data:
        return jsonify({"status": "ignored"}), 200

    message = data["message"]
    chat_id = message["chat"]["id"]
    username = message["from"].get("username", "TanpaUsername")

    if "text" in message:
        text = message["text"]

        if text == "/start":
            send_message(chat_id, f"Hai @{username}, kamu berhasil terhubung dengan bot!")
            # Simpan chat_id dan username ke DB jika perlu (panggil user_service)
            update_user_chat_id(username,chat_id)
            return jsonify({"status": "handled"}), 200

        else:
            send_message(chat_id, f"Pesanmu: {text}")
            return jsonify({"status": "handled"}), 200

    return jsonify({"status": "ignored"}), 200
