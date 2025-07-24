from flask import Blueprint, request
# from telegram import Update
# from app.services.telegram_service import app_bot

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["POST"])
def telegram_webhook():
    if request.method == "POST":
        # update = Update.de_json(request.get_json(force=True), app_bot.bot)
        # app_bot.update_queue.put_nowait(update)
        return "OK", 200
