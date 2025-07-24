import random as rnd
import MySQLdb.cursors
from flask import current_app
from app.config.database import mysql
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


def create_user(username, email, phone, password, telegram_id, chat_id=None):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_digits = str(rnd.randint(100000, 999999))
    user_id = f"USID{timestamp}{random_digits}"
    pw_hash = hash_password(password)
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (id, username, email, phone, password_hash, telegram_id, chat_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_id, username, email, phone, pw_hash, telegram_id, chat_id)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        current_app.logger.error(f"Gagal membuat user: {e}")
        return False


def get_user_by_id(user_id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user
    except Exception as e:
        current_app.logger.error(f"Gagal mengambil user berdasarkan UserId: {e}")
        return None


def get_user_by_username(username):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        return user
    except Exception as e:
        current_app.logger.error(f"Gagal mengambil user berdasarkan username: {e}")
        return None


def get_user_by_telegram(telegram_id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        user = cur.fetchone()
        cur.close()
        return user
    except Exception as e:
        current_app.logger.error(f"Gagal mengambil user berdasarkan telegram: {e}")
        return None


def get_user_by_email(email):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user
    except Exception as e:
        current_app.logger.error(f"Gagal mengambil user berdasarkan email: {e}")
        return None


def update_user_chat_id(telegram_id, chat_id):
    from app import app
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET chat_id = %s WHERE telegram_id = %s", (chat_id, telegram_id))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            current_app.logger.error(f"Gagal mengupdate chat_id user: {e}")


def delete_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        current_app.logger.error(f"Gagal menghapus user: {e}")
        return False


def hash_password(password):
    return generate_password_hash(password)


def check_password(hashed, password):
    return check_password_hash(hashed, password)
