from flask import Blueprint, render_template, request, redirect, session, flash
from datetime import datetime
from app.services.otp_service import validate_otp, remove_otp, generate_otp, otp_expiry, save_otp, check_otp
from app.services.telegram_service import send_telegram_otp
from app.services.user_service import get_user_by_username, get_user_by_id

otp_bp = Blueprint('otp', __name__)


@otp_bp.route('/otp', methods=['GET', 'POST'])
def otp():
    user_id = session.get('otp_user_id')
    if not user_id:
        return redirect('/')

    otp_check = check_otp(user_id)

    if otp_check:
        now = datetime.utcnow()
        expires_at = otp_check['expires_at']

        if request.method == 'POST':
            otp_input = request.form['otp']

            if now > expires_at:
                session['otp_expired'] = True
                session['otp_error'] = "Kode OTP telah kedaluwarsa. Silakan kirim ulang."
                return redirect('/otp')

            if validate_otp(user_id, otp_input):
                session['logged_in'] = True
                return redirect('/dashboard')
            else:
                session['otp_error'] = "Kode OTP salah."
                session['otp_expired'] = False
                return redirect('/otp')
        else:
            message = session.pop('otp_message', None)
            error = session.pop('otp_error', None)
            otp_expired = session.pop('otp_expired', False)

            if now > expires_at:
                session['otp_expired'] = True
                session['otp_message'] = "Kode OTP Anda telah kedaluwarsa. Silakan kirim ulang kode baru."
                return redirect('/otp')
            else:
                return render_template('otp.html', message=message, error=error, otp_expired=otp_expired)
    else:
        otp_expired = True
        error = "Tidak ada OTP aktif. Silakan kirim ulang kode."
        return render_template('otp.html', error=error, otp_expired=otp_expired)


@otp_bp.route('/otp/resend', methods=['POST'])
def resend():
    user_id = session.get('otp_user_id')
    if not user_id:
        return redirect('/login')

    user = get_user_by_id(user_id)

    if remove_otp(user_id):
        otp = generate_otp()
        expires_at = otp_expiry()
        save_otp(user['id'], otp, expires_at)
        send_telegram_otp(user['chat_id'], otp)

        # Simpan ke session
        session['otp_message'] = "OTP baru telah dikirim ke Telegram Anda."
        session['otp_expired'] = False

    return redirect('/otp')