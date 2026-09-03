import os
import json
from backend.app.database import ProductRepository, get_db_connection


def seed_demo_data():
    """
    Seeds realistic artisan products into SQLite database if products table is empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()

    if count > 0:
        print(f"[SEED] Database already contains {count} products. Skipping seed.")
        return

    # Find sample_products.json path
    json_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_products.json")
    json_path = os.path.abspath(json_path)

    if not os.path.exists(json_path):
        print(f"[SEED] Warning: {json_path} not found. Skipping seed.")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            ProductRepository.save(item)
        print(f"[SEED] Successfully seeded {len(items)} sample artisan products into TANTU database!")
    except Exception as e:
        print(f"[SEED] Error seeding data: {e}")
