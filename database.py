import sqlite3
import threading
import os
from cryptography.fernet import Fernet
from datetime import datetime

class RebelDatabase:
    def __init__(self, db_file, encryption_key):
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cipher = Fernet(encryption_key)
        self.lock = threading.Lock()
        self._create_tables()

    def _create_tables(self):
        with self.lock:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT,
                    email TEXT,
                    password TEXT,
                    phone TEXT,
                    cookies TEXT,
                    ip TEXT,
                    timestamp DATETIME,
                    used INTEGER DEFAULT 0,
                    reports_sent INTEGER DEFAULT 0
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT,
                    username TEXT,
                    url TEXT,
                    phone TEXT,
                    reports_sent INTEGER DEFAULT 0,
                    status TEXT,
                    added DATETIME
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS proxies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proxy TEXT,
                    last_used DATETIME,
                    failures INTEGER DEFAULT 0,
                    active INTEGER DEFAULT 1
                )
            ''')
            self.conn.commit()

    def store_credential(self, platform, email=None, password=None, phone=None, cookies='', ip=''):
        with self.lock:
            encrypted_email = self.cipher.encrypt(email.encode()).decode() if email else ''
            encrypted_password = self.cipher.encrypt(password.encode()).decode() if password else ''
            encrypted_phone = self.cipher.encrypt(phone.encode()).decode() if phone else ''
            self.cursor.execute('''
                INSERT INTO credentials (platform, email, password, phone, cookies, ip, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (platform, encrypted_email, encrypted_password, encrypted_phone, cookies, ip, datetime.now()))
            self.conn.commit()
            return self.cursor.lastrowid

    def get_unused_credentials(self, platform, limit=10):
        with self.lock:
            self.cursor.execute('''
                SELECT id, email, password, phone, cookies FROM credentials
                WHERE platform = ? AND used = 0 LIMIT ?
            ''', (platform, limit))
            rows = self.cursor.fetchall()
            decrypted = []
            for row in rows:
                decrypted.append((
                    row[0],
                    self.cipher.decrypt(row[1].encode()).decode() if row[1] else '',
                    self.cipher.decrypt(row[2].encode()).decode() if row[2] else '',
                    self.cipher.decrypt(row[3].encode()).decode() if row[3] else '',
                    row[4]
                ))
            return decrypted

    def mark_credential_used(self, cred_id):
        with self.lock:
            self.cursor.execute('UPDATE credentials SET used = 1 WHERE id = ?', (cred_id,))
            self.conn.commit()

    def add_target(self, platform, username=None, url=None, phone=None):
        with self.lock:
            self.cursor.execute('''
                INSERT INTO targets (platform, username, url, phone, status, added)
                VALUES (?, ?, ?, ?, 'pending', ?)
            ''', (platform, username, url, phone, datetime.now()))
            self.conn.commit()
            return self.cursor.lastrowid

    def increment_reports(self, target_id):
        with self.lock:
            self.cursor.execute('UPDATE targets SET reports_sent = reports_sent + 1 WHERE id = ?', (target_id,))
            self.conn.commit()

    def get_all_targets(self):
        with self.lock:
            self.cursor.execute('SELECT id, platform, username, url, phone, reports_sent, status FROM targets')
            return self.cursor.fetchall()

    def close(self):
        self.conn.close()
