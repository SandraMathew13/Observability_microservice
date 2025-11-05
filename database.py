# database.py
import sqlite3
from typing import Any, List, Tuple

DB_PATH = "observability.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        value REAL,
        timestamp TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_name TEXT,
        value REAL,
        timestamp TEXT
    )""")
    conn.commit()
    conn.close()

def insert_user(username: str, password_hash: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()

def get_user(username: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row

def insert_alert(alert_type: str, value: float, timestamp: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO alerts (type, value, timestamp) VALUES (?, ?, ?)", (alert_type, value, timestamp))
    conn.commit()
    conn.close()

def insert_metric(metric_name: str, value: float, timestamp: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO metrics (metric_name, value, timestamp) VALUES (?, ?, ?)", (metric_name, value, timestamp))
    conn.commit()
    conn.close()

def get_last_n_alerts(n: int) -> List[Tuple[Any]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT type, value, timestamp FROM alerts ORDER BY id DESC LIMIT ?", (n,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_alert_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), SUM(CASE WHEN type='CPU' THEN 1 ELSE 0 END), SUM(CASE WHEN type='Memory' THEN 1 ELSE 0 END) FROM alerts")
    row = cur.fetchone()
    conn.close()
    return row

def get_last_metrics(metric_name: str, n: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT value FROM metrics WHERE metric_name = ? ORDER BY id DESC LIMIT ?", (metric_name, n))
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows
