from flask import Blueprint, render_template, request, redirect, session, flash
from datetime import datetime
from app.services.otp_service import validate_otp, get_latest_otp, generate_and_send_otp
from app.services.user_service import get_user_by_username

otp_bp = Blueprint('otp', __name__)


@otp_bp.route('/otp', methods=['GET', 'POST'])
def otp_verify():
    user_id = session.get('otp_user_id')
    chat_id = session.get('otp_chat_id')

    if not user_id or not chat_id:
        flash("Sesi OTP tidak ditemukan. Silakan login ulang.", "warning")
        return redirect('/login')

    latest_otp = get_latest_otp(user_id)

    if not latest_otp:
        flash("Tidak ada OTP aktif. Silakan kirim ulang.", "danger")
        return redirect('/login')

    now = datetime.utcnow()

    if request.method == 'POST':
        otp_input = request.form.get('otp')
        if now > latest_otp['expires_at']:
            flash("Kode OTP telah kedaluwarsa. Silakan minta OTP baru.", "danger")
            return render_template('otp.html', otp_expired=True)

        if validate_otp(user_id, otp_input):
            # Login berhasil
            session['user_id'] = user_id
            session['username'] = get_user_by_username(user_id)['username']
            session.pop('otp_user_id', None)
            session.pop('otp_chat_id', None)
            return redirect('/dashboard')
        else:
            flash("Kode OTP salah. Silakan coba lagi.", "danger")
            return render_template('otp.html', otp_expired=False)

    # GET method
    if now > latest_otp['expires_at']:
        flash("Kode OTP Anda telah kedaluwarsa. Silakan minta OTP baru.", "warning")
        return render_template('otp.html', otp_expired=True)

    flash("Kode OTP telah dikirim ke Telegram Anda.", "info")
    return render_template('otp.html', otp_expired=False)


@otp_bp.route('/otp/resend', methods=['GET'])
def resend_otp():
    user_id = session.get('otp_user_id')
    chat_id = session.get('otp_chat_id')

    if not user_id or not chat_id:
        flash("Sesi tidak valid. Silakan login ulang.", "warning")
        return redirect('/login')

    if generate_and_send_otp(user_id, chat_id):
        flash("Kode OTP baru telah dikirim ke Telegram Anda.", "success")
    else:
        flash("Gagal mengirim OTP. Periksa koneksi bot Telegram Anda.", "danger")

    return redirect('/otp')
