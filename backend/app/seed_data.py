import os
import json
from backend.app.database import (
    ProductRepository,
    ArtisanProfileRepository,
    BuyerRepository,
    UserRepository,
    get_db_connection
)


def seed_demo_data():
    """
    Seeds realistic artisan products, users, profiles, and buyers into SQLite database if products table is empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()

    if count > 0:
        print(f"[SEED] Database already contains {count} products. Skipping seed.")
        return

    # Seed demo users and artisan profiles
    demo_artisans = [
        {
            "id": "art-001",
            "user_id": "art-001",
            "artisan_name": "Lakshmi Devi",
            "craft_type": "Bamboo & Natural Fiber Crafting",
            "location": "Silchar, Cachar District, Assam",
            "bio": "Master artisan with 20+ years of experience crafting eco-friendly bamboo items.",
            "phone": "+91-9876543210",
            "story_style": "Cultural Heritage"
        },
        {
            "id": "art-002",
            "user_id": "art-002",
            "artisan_name": "Ramesh Ansari",
            "craft_type": "Chanderi Handloom Weaving",
            "location": "Chanderi, Ashoknagar District, Madhya Pradesh",
            "bio": "Fourth-generation handloom weaver specializing in fine silk-cotton fabrics and golden zari work.",
            "phone": "+91-9876543211",
            "story_style": "Artisanal Mastery"
        },
        {
            "id": "art-003",
            "user_id": "art-003",
            "artisan_name": "Suresh Sharma",
            "craft_type": "Saharanpur Wood Carving",
            "location": "Saharanpur, Uttar Pradesh",
            "bio": "Expert wood craftsman preserving centuries-old brass inlay and relief carving techniques.",
            "phone": "+91-9876543212",
            "story_style": "Heritage Craftsmanship"
        },
        {
            "id": "art-004",
            "user_id": "art-004",
            "artisan_name": "Pinki Kumawat",
            "craft_type": "Jaipur Blue Pottery",
            "location": "Jaipur, Rajasthan",
            "bio": "Passionate artisan carrying forward royal Jaipur blue pottery heritage.",
            "phone": "+91-9876543213",
            "story_style": "Royal Heritage"
        }
    ]

    for art in demo_artisans:
        UserRepository.save({
            "id": art["user_id"],
            "name": art["artisan_name"],
            "phone": art["phone"],
            "role": "artisan",
            "region": art["location"]
        })
        ArtisanProfileRepository.save(art)

    # Seed demo buyers
    demo_buyers = [
        {
            "id": "buyer-001",
            "user_id": "user-buyer-001",
            "buyer_name": "FabIndia Procurement Team",
            "organization": "FabIndia Overseas Pvt Ltd",
            "buyer_type": "B2B Retailer",
            "contact_email": "procurement@fabindia.com"
        },
        {
            "id": "buyer-002",
            "user_id": "user-buyer-002",
            "buyer_name": "Kraft Emporium Global",
            "organization": "Kraft Emporium Export House",
            "buyer_type": "Wholesaler",
            "contact_email": "export@kraftemporium.com"
        }
    ]

    for b in demo_buyers:
        UserRepository.save({
            "id": b["user_id"],
            "name": b["buyer_name"],
            "phone": "+91-9988776655",
            "role": "buyer",
            "region": "New Delhi"
        })
        BuyerRepository.save(b)

    # Find sample_products.json path
    json_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_products.json")
    json_path = os.path.abspath(json_path)

    if not os.path.exists(json_path):
        print(f"[SEED] Warning: {json_path} not found. Skipping product seed.")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            if "status" not in item:
                item["status"] = "published"
            ProductRepository.save(item)
        print(f"[SEED] Successfully seeded {len(items)} sample artisan products into TANTU database!")
    except Exception as e:
        print(f"[SEED] Error seeding data: {e}")


