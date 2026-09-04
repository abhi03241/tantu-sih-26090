import os
import json
from backend.app.database import (
    ProductRepository,
    ArtisanRepository,
    BuyerRepository,
    OrderRepository,
    get_db_connection
)


def seed_demo_data():
    """
    Seeds realistic artisan products, artisan profiles, buyer organizations,
    and B2B order requests into SQLite database if tables are empty.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

    # 1. Seed Products
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM artisan_profiles")
    artisan_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM buyers")
    buyer_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    conn.close()

    # Seed Products
    if product_count == 0:
        products_file = os.path.join(data_dir, "sample_products.json")
        if os.path.exists(products_file):
            try:
                with open(products_file, "r", encoding="utf-8") as f:
                    products = json.load(f)
                for item in products:
                    ProductRepository.save(item)
                print(f"[SEED] Successfully seeded {len(products)} sample artisan products into database.")
            except Exception as e:
                print(f"[SEED] Error seeding products: {e}")
    else:
        print(f"[SEED] Database already contains {product_count} products. Skipping product seed.")

    # Seed Artisans
    if artisan_count == 0:
        artisans_file = os.path.join(data_dir, "sample_artisans.json")
        if os.path.exists(artisans_file):
            try:
                with open(artisans_file, "r", encoding="utf-8") as f:
                    artisans = json.load(f)
                for art in artisans:
                    ArtisanRepository.save(art)
                print(f"[SEED] Successfully seeded {len(artisans)} artisan profiles into database.")
            except Exception as e:
                print(f"[SEED] Error seeding artisans: {e}")
    else:
        print(f"[SEED] Database already contains {artisan_count} artisan profiles. Skipping artisan seed.")

    # Seed Buyers
    if buyer_count == 0:
        buyers_file = os.path.join(data_dir, "sample_buyers.json")
        if os.path.exists(buyers_file):
            try:
                with open(buyers_file, "r", encoding="utf-8") as f:
                    buyers = json.load(f)
                for buyer in buyers:
                    BuyerRepository.save(buyer)
                print(f"[SEED] Successfully seeded {len(buyers)} buyer profiles into database.")
            except Exception as e:
                print(f"[SEED] Error seeding buyers: {e}")
    else:
        print(f"[SEED] Database already contains {buyer_count} buyers. Skipping buyer seed.")

    # Seed Orders
    if order_count == 0:
        orders_file = os.path.join(data_dir, "sample_orders.json")
        if os.path.exists(orders_file):
            try:
                with open(orders_file, "r", encoding="utf-8") as f:
                    orders = json.load(f)
                for order in orders:
                    OrderRepository.save(order)
                print(f"[SEED] Successfully seeded {len(orders)} sample B2B orders into database.")
            except Exception as e:
                print(f"[SEED] Error seeding orders: {e}")
    else:
        print(f"[SEED] Database already contains {order_count} orders. Skipping order seed.")
