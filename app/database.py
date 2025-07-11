import sqlite3
from datetime import datetime
from typing import Optional, List
from app.models import Product, PriceHistory

DATABASE_URL = "price_bot.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("[DB] Verificando e inicializando o banco de dados para histórico...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            scrape_date TIMESTAMP NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("[DB] Banco de dados pronto.")

def add_scrape_results(scraped_data: list[dict]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    new_price_entries = 0
    for item in scraped_data:
        cursor.execute("SELECT id FROM products WHERE link = ?", (item['link'],))
        product_row = cursor.fetchone()
        
        product_id = None
        if product_row:
            product_id = product_row['id']
        else:
            cursor.execute(
                "INSERT INTO products (title, link) VALUES (?, ?)",
                (item['title'], item['link'])
            )
            product_id = cursor.lastrowid
        
        if product_id:
            cursor.execute(
                "INSERT INTO price_history (product_id, price, scrape_date) VALUES (?, ?, ?)",
                (product_id, item['price'], datetime.now())
            )
            new_price_entries += 1
            
    conn.commit()
    conn.close()
    print(f"[DB] Processamento finalizado. {new_price_entries} novos registros de preço adicionados.")

def get_all_products_with_latest_price() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.id,
            p.title,
            p.link,
            (SELECT ph.price FROM price_history ph WHERE ph.product_id = p.id ORDER BY ph.scrape_date DESC LIMIT 1) as latest_price
        FROM products p
    """
    cursor.execute(query)
    products = cursor.fetchall()
    conn.close()
    return [dict(row) for row in products]

def get_product_history(product_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, link FROM products WHERE id = ?", (product_id,))
    product_info = cursor.fetchone()

    if not product_info:
        return None

    cursor.execute(
        "SELECT price, scrape_date FROM price_history WHERE product_id = ? ORDER BY scrape_date DESC",
        (product_id,)
    )
    history = cursor.fetchall()
    conn.close()

    return {
        "product": dict(product_info),
        "history": [dict(row) for row in history]
    }


init_db()

