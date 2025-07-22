import os

from flask import Flask
from app.config.database import init_mysql

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'defaultsecret')

    # Inisialisasi database
    init_mysql(app)

    # Import dan register blueprint lainnya
    from app.routes import auth, dashboard, webhook
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(dashboard.dashboard_bp)
    app.register_blueprint(webhook.webhook_bp)

    return app
