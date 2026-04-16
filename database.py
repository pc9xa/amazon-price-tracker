import os
import pandas as pds
from dotenv import load_dotenv
from pandas.errors import DatabaseError
from sqlalchemy import create_engine, text

# - Initialize -------------------------------------------------------------------
# - Local environment only
load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH")

# - Database communication -------------------------------------------------------
def get_connection():
    return create_engine(DB_PATH).connect()

def init_db():
    with get_connection() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                product_name TEXT,
                product_link TEXT,
                price REAL,
                timestamp TEXT
            )
        """))
        conn.commit()

def save_price(product, product_link, price, timestamp):
    with get_connection() as conn:
        conn.execute(
            text("INSERT INTO prices (product_name, product_link, price, timestamp) VALUES (:product, :price, :timestamp)"),
            {"product": product, "product_link": product_link, "price": price, "timestamp": timestamp}
        )

        conn.commit()

def load_tracked_products():
    with get_connection() as conn:
        query = "SELECT DISTINCT product_name FROM prices"

        try:
            df = pds.read_sql(query, conn)
        except DatabaseError as e:
            return f"Error occurred while loading the monitored products:\n {e}"
        else:
            return df["product_name"].to_list()

def load_product_prices(product):
    with get_connection() as conn:
        query = text("""
            SELECT * FROM prices
            WHERE product_name = :product            
            ORDER BY timestamp DESC
        """)

        df = pds.read_sql(query, conn, params={"product": product})
        return df

def del_product(product):
    with get_connection() as conn:
        conn.execute(
            text("DELETE FROM prices WHERE product_name = :product"),
            {"product": product},
        )
        conn.commit()