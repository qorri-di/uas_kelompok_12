from flask import Blueprint, request, jsonify
from app.services.telegram_service import set_webhook, handle_message, send_message

webhook_bp = Blueprint('webhook_bp', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def telegram_webhook():
    """
    Endpoint utama untuk menerima update dari Telegram (webhook).
    Akan memanggil handle_message dari service.
    """
    data = request.get_json()
    if not data:
        return jsonify({'status': 'No JSON received'}), 400

    return handle_message(data)


@webhook_bp.route('/set-webhook', methods=['GET'])
def webhook_setup():
    """
    Endpoint manual untuk menyetel webhook ke Telegram.
    Cukup akses /set-webhook sekali dari browser atau Postman.
    """
    success = set_webhook()
    if success:
        return jsonify({'status': 'Webhook berhasil disetel'}), 200
    else:
        return jsonify({'status': 'Gagal menyetel webhook'}), 500


@webhook_bp.route('/send-test/<chat_id>', methods=['GET'])
def send_test(chat_id):
    """
    Endpoint untuk menguji pengiriman pesan ke chat_id tertentu.
    """
    test_text = "✅ Ini adalah pesan uji coba dari Flask Telegram Bot"
    success = send_message(chat_id, test_text)

    if success:
        return jsonify({'status': 'Pesan uji berhasil dikirim'}), 200
    else:
        return jsonify({'status': 'Gagal mengirim pesan uji'}), 500
