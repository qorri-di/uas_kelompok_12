from flask import current_app
from app.config.database import mysql
from datetime import datetime, timedelta
from app.services.telegram_service import send_message
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
        cur.execute("""
            INSERT INTO otp_tokens (user_id, otp_code, is_used, expires_at)
            VALUES (%s, %s, %s, %s)
        """, (user_id, otp, False, expires_at))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        current_app.logger.error(f"Gagal menyimpan OTP: {e}")
        return False


def check_otp(user_id):
    """Ambil OTP aktif berdasarkan user"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT * FROM otp_tokens
            WHERE user_id = %s AND is_used = FALSE
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))
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
        cur.execute("""
            SELECT id, expires_at FROM otp_tokens
            WHERE user_id = %s AND otp = %s AND is_used = FALSE
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id, input_otp))
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
        cur.execute("""
            DELETE FROM otp_tokens
            WHERE user_id = %s AND is_used = FALSE
        """, (user_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        current_app.logger.error(f"Gagal menghapus OTP yang belum dipakai: {e}")
        return False


def generate_and_send_otp(user_id, chat_id):
    """Generate dan kirim OTP ke Telegram user."""
    try:
        remove_otp(user_id)  # Pastikan hanya ada 1 OTP aktif
        otp_code = generate_otp()
        expires_at = otp_expiry()
        save_otp(user_id, otp_code, expires_at)
        message = f"Kode OTP Anda adalah: {otp_code}. Berlaku selama 5 menit."
        return send_message(chat_id, message)
    except Exception as e:
        print(f"[ERROR] Gagal mengirim OTP: {e}")
        return False


def get_latest_otp(user_id):
    """
    Mengambil OTP terakhir yang belum digunakan untuk user_id tertentu.
    """
    try:
        cur = mysql.connection.cursor()
        query = """
            SELECT id, user_id, otp_code, expires_at, is_used
            FROM otp_tokens
            WHERE user_id = %s AND is_used = FALSE
            ORDER BY expires_at DESC
            LIMIT 1
            """
        cur.execute(query, (user_id,))
        row = cur.fetchone()
        cur.close()

        if row:
            return {
                'id': row[0],
                'user_id': row[1],
                'otp_code': row[2],
                'expires_at': row[3],
                'is_used': row[4]
            }
        else:
            return None
    except Exception as e:
        current_app.logger.error(f"Gagal mengambil OTP terbaru: {e}")
        return None