import sqlite3
import pandas as pds
from pathlib import Path

DB_PATH = Path("data/prices.db")

def get_connection():
    return sqlite3.connect(DB_PATH, timeout=20)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                price REAL,
                timestamp TEXT
            )
        """)

def save_price(product, price, timestamp):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO prices (product_name, price, timestamp) VALUES (?, ?, ?)",
            (product, price, timestamp)
        )

        conn.commit()

def load_tracked_products():
    with get_connection() as conn:
        query = "SELECT DISTINCT product_name FROM prices"
        df = pds.read_sql(query, conn)
        product_list = df["product_name"].to_list()
        return product_list

def load_product_prices(product):
    with get_connection() as conn:
        query = """
            SELECT * FROM prices
            WHERE product_name = ?            
            ORDER BY timestamp DESC
        """

        df = pds.read_sql(query, conn, params=(product,))
        return df

def del_product(product):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM prices WHERE product_name = ?",
            (product,),
        )