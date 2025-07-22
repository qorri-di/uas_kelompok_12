from flask_mysqldb import MySQL
from flask import Flask
import os

mysql = MySQL()


def init_mysql(app: Flask):
    """Konfigurasi koneksi database MySQL untuk Flask app"""
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'your_database')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))

    mysql.init_app(app)
    return mysql
