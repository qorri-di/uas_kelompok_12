import threading
from app import create_app
from app.services.telegram_service import run_telegram_bot

app = create_app()

if __name__ == '__main__':
    # Jalankan telegram bot di thread terpisah
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()

    # Jalankan Flask di thread utama
    app.run(debug=True, use_reloader=False)  # Jangan pakai reloader agar event loop tetap ada
