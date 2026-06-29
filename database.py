import sqlite3
from datetime import datetime

DB_FILE = "tracker.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            item_id TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            url TEXT,
            seller TEXT,
            timestamp TEXT,
            first_seen TEXT
        )
    """)

    conn.commit()
    conn.close()


def is_new_item(item_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM listings WHERE item_id = ?", (item_id,))
    exists = cur.fetchone() is not None

    conn.close()

    return not exists


def save_item(item):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO listings (
            item_id, title, price, url, seller, timestamp, first_seen
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        item["item_id"],
        item["title"],
        item["price"],
        item["url"],
        item["seller"],
        item["timestamp"],
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
