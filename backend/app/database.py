import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.app.config import settings


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes SQLite tables for products, users, artisan profiles, buyers, and order requests.
    Performs backward-compatible schema migrations if tables already exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description_english TEXT,
        description_hindi TEXT,
        category TEXT,
        material TEXT,
        dimensions TEXT,
        production_time TEXT,
        tags TEXT,
        story TEXT,
        sentiment TEXT,
        narrative_type TEXT,
        image_url TEXT,
        enhanced_image_url TEXT,
        suggested_price_min REAL,
        suggested_price_max REAL,
        artisan_id TEXT,
        artisan_name TEXT,
        location TEXT,
        status TEXT DEFAULT 'draft',
        created_at TEXT
    )
    """)

    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        role TEXT,
        region TEXT,
        created_at TEXT
    )
    """)

    # Create Artisan Profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artisan_profiles (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        artisan_name TEXT,
        name TEXT,
        craft_type TEXT,
        location TEXT,
        language TEXT,
        bio TEXT,
        phone TEXT,
        contact TEXT,
        story_style TEXT
    )
    """)

    # Create Buyers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buyers (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        buyer_name TEXT,
        name TEXT,
        organization TEXT,
        buyer_type TEXT,
        contact_email TEXT,
        contact TEXT,
        phone TEXT
    )
    """)

    # Create Order Requests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        product_id TEXT,
        product_title TEXT,
        artisan_id TEXT,
        buyer_id TEXT,
        buyer_name TEXT,
        buyer_contact TEXT,
        quantity INTEGER,
        notes TEXT,
        message TEXT,
        price_offered REAL,
        status TEXT,
        created_at TEXT
    )
    """)

    # Schema migration checks for existing tables
    def ensure_column(table_name: str, column_name: str, col_type: str):
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_cols = [row["name"] for row in cursor.fetchall()]
        if column_name not in existing_cols:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {col_type}")

    # Migrations for artisan_profiles
    ensure_column("artisan_profiles", "name", "TEXT")
    ensure_column("artisan_profiles", "language", "TEXT")
    ensure_column("artisan_profiles", "contact", "TEXT")

    # Migrations for products
    ensure_column("products", "status", "TEXT DEFAULT 'draft'")

    # Migrations for buyers
    ensure_column("buyers", "name", "TEXT")
    ensure_column("buyers", "contact", "TEXT")
    ensure_column("buyers", "phone", "TEXT")

    # Migrations for orders
    ensure_column("orders", "buyer_id", "TEXT")
    ensure_column("orders", "message", "TEXT")

    conn.commit()
    conn.close()


class ProductRepository:
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        if not d.get("status"):
            d["status"] = "draft"
        if d.get("tags"):
            try:
                d["tags"] = json.loads(d["tags"])
            except Exception:
                d["tags"] = [t.strip() for t in d["tags"].split(",") if t.strip()]
        else:
            d["tags"] = []
        return d

    @classmethod
    def get_all(cls, category: Optional[str] = None, artisan_id: Optional[str] = None, query: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM products WHERE 1=1"
        params = []

        if category:
            sql += " AND lower(category) LIKE lower(?)"
            params.append(f"%{category}%")
        if artisan_id:
            sql += " AND artisan_id = ?"
            params.append(artisan_id)
        if status:
            sql += " AND lower(status) = lower(?)"
            params.append(status)
        if query:
            sql += " AND (lower(title) LIKE lower(?) OR lower(description_english) LIKE lower(?) OR lower(description_hindi) LIKE lower(?) OR lower(material) LIKE lower(?) OR lower(tags) LIKE lower(?))"
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"])

        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [cls._row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, product_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        return cls._row_to_dict(row) if row else None

    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        tags_str = json.dumps(data.get("tags", []))
        created_at = data.get("created_at") or datetime.now().isoformat()
        prod_status = data.get("status") or "draft"

        cursor.execute("""
        INSERT INTO products (
            id, title, description_english, description_hindi, category, material,
            dimensions, production_time, tags, story, sentiment, narrative_type,
            image_url, enhanced_image_url, suggested_price_min, suggested_price_max,
            artisan_id, artisan_name, location, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            description_english=excluded.description_english,
            description_hindi=excluded.description_hindi,
            category=excluded.category,
            material=excluded.material,
            dimensions=excluded.dimensions,
            production_time=excluded.production_time,
            tags=excluded.tags,
            story=excluded.story,
            sentiment=excluded.sentiment,
            narrative_type=excluded.narrative_type,
            image_url=excluded.image_url,
            enhanced_image_url=excluded.enhanced_image_url,
            suggested_price_min=excluded.suggested_price_min,
            suggested_price_max=excluded.suggested_price_max,
            artisan_id=excluded.artisan_id,
            artisan_name=excluded.artisan_name,
            location=excluded.location,
            status=excluded.status
        """, (
            data["id"],
            data["title"],
            data.get("description_english", ""),
            data.get("description_hindi", ""),
            data.get("category", "Handicraft"),
            data.get("material", "Natural Material"),
            data.get("dimensions"),
            data.get("production_time"),
            tags_str,
            data.get("story"),
            data.get("sentiment"),
            data.get("narrative_type"),
            data.get("image_url", ""),
            data.get("enhanced_image_url"),
            data.get("suggested_price_min"),
            data.get("suggested_price_max"),
            data.get("artisan_id", "art-001"),
            data.get("artisan_name", "Artisan"),
            data.get("location", "India"),
            prod_status,
            created_at
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])

    @classmethod
    def update_status(cls, product_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET status = ? WHERE id = ?", (new_status, product_id))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return cls.get_by_id(product_id) if updated else None

    @classmethod
    def delete(cls, product_id: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted


class ArtisanRepository:
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        # Harmonize name and contact placeholders
        if not d.get("name") and d.get("artisan_name"):
            d["name"] = d["artisan_name"]
        if not d.get("artisan_name") and d.get("name"):
            d["artisan_name"] = d["name"]
        if not d.get("contact") and d.get("phone"):
            d["contact"] = d["phone"]
        if not d.get("phone") and d.get("contact"):
            d["phone"] = d["contact"]
        return d

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artisan_profiles ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return [cls._row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, artisan_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artisan_profiles WHERE id = ? OR user_id = ?", (artisan_id, artisan_id))
        row = cursor.fetchone()
        conn.close()
        return cls._row_to_dict(row) if row else None

    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()

        artisan_id = data.get("id") or f"prof-{data.get('user_id', 'art-001')}"
        user_id = data.get("user_id") or artisan_id
        artisan_name = data.get("artisan_name") or data.get("name", "Artisan")
        name = data.get("name") or artisan_name
        phone = data.get("phone") or data.get("contact", "")
        contact = data.get("contact") or phone

        cursor.execute("""
        INSERT INTO artisan_profiles (
            id, user_id, artisan_name, name, craft_type, location, language, bio, phone, contact, story_style
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            user_id=excluded.user_id,
            artisan_name=excluded.artisan_name,
            name=excluded.name,
            craft_type=excluded.craft_type,
            location=excluded.location,
            language=excluded.language,
            bio=excluded.bio,
            phone=excluded.phone,
            contact=excluded.contact,
            story_style=excluded.story_style
        """, (
            artisan_id,
            user_id,
            artisan_name,
            name,
            data.get("craft_type", "Handicraft"),
            data.get("location", "India"),
            data.get("language", "Hindi"),
            data.get("bio", ""),
            phone,
            contact,
            data.get("story_style", "Cultural Heritage")
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(artisan_id)


class BuyerRepository:
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        if not d.get("name") and d.get("buyer_name"):
            d["name"] = d["buyer_name"]
        if not d.get("buyer_name") and d.get("name"):
            d["buyer_name"] = d["name"]
        if not d.get("contact") and d.get("contact_email"):
            d["contact"] = d["contact_email"]
        return d

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buyers ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return [cls._row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, buyer_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buyers WHERE id = ? OR user_id = ?", (buyer_id, buyer_id))
        row = cursor.fetchone()
        conn.close()
        return cls._row_to_dict(row) if row else None

    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()

        buyer_id = data.get("id") or f"buy-{data.get('user_id', 'buyer-001')}"
        user_id = data.get("user_id") or buyer_id
        buyer_name = data.get("buyer_name") or data.get("name", "B2B Buyer")
        name = data.get("name") or buyer_name
        contact_email = data.get("contact_email") or data.get("contact", "")
        contact = data.get("contact") or contact_email
        phone = data.get("phone", "")

        cursor.execute("""
        INSERT INTO buyers (
            id, user_id, buyer_name, name, organization, buyer_type, contact_email, contact, phone
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            user_id=excluded.user_id,
            buyer_name=excluded.buyer_name,
            name=excluded.name,
            organization=excluded.organization,
            buyer_type=excluded.buyer_type,
            contact_email=excluded.contact_email,
            contact=excluded.contact,
            phone=excluded.phone
        """, (
            buyer_id,
            user_id,
            buyer_name,
            name,
            data.get("organization", "Retail House"),
            data.get("buyer_type", "B2B"),
            contact_email,
            contact,
            phone
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(buyer_id)


class OrderRepository:
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        # Synchronize notes and message
        if not d.get("message") and d.get("notes"):
            d["message"] = d["notes"]
        if not d.get("notes") and d.get("message"):
            d["notes"] = d["message"]
        return d

    @classmethod
    def get_all(cls, product_id: Optional[str] = None, artisan_id: Optional[str] = None, buyer_id: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM orders WHERE 1=1"
        params = []
        if product_id:
            sql += " AND product_id = ?"
            params.append(product_id)
        if artisan_id:
            sql += " AND artisan_id = ?"
            params.append(artisan_id)
        if buyer_id:
            sql += " AND buyer_id = ?"
            params.append(buyer_id)
        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [cls._row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, order_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        return cls._row_to_dict(row) if row else None

    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = data.get("created_at") or datetime.now().isoformat()
        notes = data.get("notes") or data.get("message", "")
        message = data.get("message") or notes

        cursor.execute("""
        INSERT INTO orders (
            id, product_id, product_title, artisan_id, buyer_id, buyer_name, buyer_contact,
            quantity, notes, message, price_offered, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            product_id=excluded.product_id,
            product_title=excluded.product_title,
            artisan_id=excluded.artisan_id,
            buyer_id=excluded.buyer_id,
            buyer_name=excluded.buyer_name,
            buyer_contact=excluded.buyer_contact,
            quantity=excluded.quantity,
            notes=excluded.notes,
            message=excluded.message,
            price_offered=excluded.price_offered,
            status=excluded.status
        """, (
            data["id"],
            data["product_id"],
            data.get("product_title", ""),
            data.get("artisan_id", ""),
            data.get("buyer_id"),
            data["buyer_name"],
            data["buyer_contact"],
            data["quantity"],
            notes,
            message,
            data.get("price_offered"),
            data.get("status", "pending"),
            created_at
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])

    @classmethod
    def update_status(cls, order_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return cls.get_by_id(order_id) if updated else None
