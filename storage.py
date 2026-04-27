import sqlite3
import json
from datetime import datetime

DB_NAME = "runs.db"

def init_db():
    """Prépare le terrain en créant la table si elle n'existe pas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            passed INTEGER,
            failed INTEGER,
            latency_avg REAL,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_run(summary, tests_details):
    """Enregistre le résultat final du round."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO test_runs (timestamp, passed, failed, latency_avg, details)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        summary['passed'],
        summary['failed'],
        summary['latency_ms_avg'],
        json.dumps(tests_details) # On stocke le détail en JSON dans la base
    ))
    conn.commit()
    conn.close()
