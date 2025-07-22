import os
from flask import Flask
from app.config.database import init_mysql
# import asyncio
# from app.config.telegram import WEBHOOK_ENDPOINT
# from app.services.telegram_service import app_bot, run_telegram_bot


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'defaultsecret')

    # Inisialisasi database
    init_mysql(app)

    # Import dan register blueprint lainnya
    from app.routes import auth, dashboard, otp, webhook
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(dashboard.dashboard_bp)
    app.register_blueprint(otp.otp_bp)
    app.register_blueprint(webhook.webhook_bp)

    # Atur handler Telegram
    # run_telegram_bot()

    # Set webhook Telegram
    # async def set_webhook():
    #     await app_bot.bot.set_webhook(url=WEBHOOK_ENDPOINT)
    #
    # asyncio.run(set_webhook())

    return app
