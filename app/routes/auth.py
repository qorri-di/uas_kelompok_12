from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.user_service import create_user, get_user_by_username
from app.services.otp_service import generate_and_send_otp

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        telegram_username = request.form.get('telegram_username')

        if not username or not password or not telegram_username:
            flash('Semua kolom wajib diisi.', 'error')
            return redirect('/register')

        existing_user = get_user_by_username(username)
        if existing_user:
            flash('Username sudah terdaftar.', 'error')
            return redirect('/register')

        hashed_password = generate_password_hash(password)
        create_user(username, hashed_password, telegram_username)
        flash('Pendaftaran berhasil. Silakan login.', 'success')
        return redirect('/')

    return render_template('register.html', title='Register')


@auth_bp.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_username(username)
        if not user or not check_password_hash(user['password'], password):
            error = "Username atau password salah."
            flash('Username atau password salah.', 'error')
            return redirect('/login')

        session['otp_user_id'] = user['id']
        session['otp_expired'] = False

        # Kirim OTP via Telegram
        otp_success = generate_and_send_otp(user['id'], user['chat_id'])
        if otp_success:
            flash('Kode OTP telah dikirim ke Telegram Anda.', 'info')
        else:
            flash('Gagal mengirim OTP.', 'error')

        return redirect('/otp')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')