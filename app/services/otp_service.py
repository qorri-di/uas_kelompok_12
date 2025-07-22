import MySQLdb
from flask import current_app
from app.config.database import mysql
from datetime import datetime, timedelta
import random


def generate_otp(length=6):
    """Generate a numeric OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def otp_expiry(minutes=5):
    """Generate OTP expiration time (default 5 minutes from now)"""
    return datetime.utcnow() + timedelta(minutes=minutes)


def save_otp(user_id, otp, expires_at):
    """Simpan OTP ke database"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO otp_tokens (user_id, otp_code, is_used, expires_at) VALUES (%s, %s, %s, %s)",
                    (user_id, otp, False, expires_at))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        current_app.logger.error(f"Gagal menyimpan OTP: {e}")
        return False


def check_otp(user_id):
    """Ambil OTP aktif berdasarkan user"""
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM otp_tokens WHERE user_id = %s AND is_used = FALSE ORDER BY created_at DESC LIMIT 1",
                    (user_id,))
        otp = cur.fetchone()
        cur.close()
        return otp
    except Exception as e:
        current_app.logger.error(f"Gagal mengambil OTP: {e}")
        return None


def validate_otp(user_id, input_otp):
    """Validasi OTP dan tandai sebagai digunakan"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, expires_at FROM otp_tokens WHERE user_id = %s AND otp_code = %s AND is_used = FALSE ORDER BY created_at DESC LIMIT 1",
                    (user_id, input_otp))
        otp = cur.fetchone()

        if otp:
            otp_id, expires_at = otp
            if datetime.utcnow() > expires_at:
                return False

            # Update is_used = TRUE
            cur.execute("UPDATE otp_tokens SET is_used = TRUE WHERE id = %s", (otp_id,))
            mysql.connection.commit()
            cur.close()
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"Validasi OTP gagal: {e}")
        return False


def remove_otp(user_id):
    """Hapus OTP aktif yang belum digunakan"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM otp_tokens WHERE user_id = %s AND is_used = FALSE", (user_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        current_app.logger.error(f"Gagal menghapus OTP yang belum dipakai: {e}")
        return False
