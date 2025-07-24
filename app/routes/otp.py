from flask import Blueprint, render_template, request, redirect, session
from app.services.otp_service import validate_otp, check_otp

otp_bp = Blueprint('otp', __name__)


@otp_bp.route('/otp', methods=['GET', 'POST'])
def otp():
    user_id = session.get('otp_user_id')
    message = session.pop('otp_message', None)
    error = session.pop('otp_error', None)

    if not user_id:
        return redirect('/')

    otp_check = check_otp(user_id)

    if otp_check:
        if request.method == 'POST':
            otp_input = request.form['otp']

            if validate_otp(user_id, otp_input):
                session['logged_in'] = True
                return render_template('dashboard.html')
            else:
                session['otp_error'] = "Kode OTP salah."
                session['otp_expired'] = False
                return redirect('/otp')
        else:
            return render_template('otp.html', message=message, error=error)
    else:
        return render_template('otp.html', message=message, error=error)
