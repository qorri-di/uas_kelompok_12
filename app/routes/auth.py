from flask import Blueprint, render_template, request, redirect, session, flash
from app.services.telegram_service import send_telegram_otp
from app.services.user_service import create_user, get_user_by_username, check_password
from app.services.otp_service import generate_otp, otp_expiry, save_otp

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        telegram_chat_id = request.form['telegram']
        create_user(username, email, phone, password, telegram_chat_id)
        return redirect('/')
    return redirect('/register')


@auth_bp.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login_redirect():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password(user['password_hash'], password):
            otp = generate_otp()
            expires_at = otp_expiry()

            session['otp_user_id'] = user['id']
            session['otp_expired'] = False

            save_otp(user['id'], otp, expires_at)
            send_telegram_otp(user['chat_id'], otp)
            return redirect('/otp')
        else:
            error = "Username atau password salah."
            return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')