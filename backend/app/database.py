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
        status TEXT DEFAULT 'published',
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
        craft_type TEXT,
        location TEXT,
        bio TEXT,
        phone TEXT,
        story_style TEXT
    )
    """)

    # Create Buyers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buyers (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        buyer_name TEXT,
        organization TEXT,
        buyer_type TEXT,
        contact_email TEXT
    )
    """)

    # Create Order Requests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        product_id TEXT,
        product_title TEXT,
        artisan_id TEXT,
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

    # Safety migration for existing databases missing message column
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN message TEXT")
    except Exception:
        pass

    # Safety migration for existing databases missing status column on products
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN status TEXT DEFAULT 'published'")
    except Exception:
        pass

    try:
        cursor.execute("UPDATE products SET status = 'published' WHERE status IS NULL")
    except Exception:
        pass

    conn.commit()
    conn.close()


class ProductRepository:
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        if not d.get("status"):
            d["status"] = "published"
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

        if status:
            sql += " AND lower(COALESCE(status, 'published')) = lower(?)"
            params.append(status)
        if category:
            sql += " AND lower(category) LIKE lower(?)"
            params.append(f"%{category}%")
        if artisan_id:
            sql += " AND artisan_id = ?"
            params.append(artisan_id)
        if query:
            sql += " AND (lower(title) LIKE lower(?) OR lower(description_english) LIKE lower(?) OR lower(material) LIKE lower(?))"
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

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
            data.get("status") or "published",
            created_at
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])


class OrderRepository:
    @staticmethod
    def _row_to_order_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        msg = d.get("message")
        notes = d.get("notes")
        # Ensure both message and notes are synchronized for all consumers
        if not msg and notes:
            d["message"] = notes
        elif not notes and msg:
            d["notes"] = msg
        return d

    @classmethod
    def get_all(cls, product_id: Optional[str] = None, artisan_id: Optional[str] = None) -> List[Dict[str, Any]]:
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
        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [cls._row_to_order_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, order_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        return cls._row_to_order_dict(row) if row else None

    @classmethod
    def update_status(cls, order_id: str, status: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        conn.commit()
        conn.close()
        return cls.get_by_id(order_id)

    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = data.get("created_at") or datetime.now().isoformat()
        data["created_at"] = created_at
        msg = data.get("message") or data.get("notes")
        notes = data.get("notes") or data.get("message")

        cursor.execute("""
        INSERT INTO orders (
            id, product_id, product_title, artisan_id, buyer_name, buyer_contact,
            quantity, notes, message, price_offered, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"],
            data["product_id"],
            data.get("product_title", ""),
            data.get("artisan_id", ""),
            data["buyer_name"],
            data.get("buyer_contact", "procurement@buyer.com"),
            data["quantity"],
            notes,
            msg,
            data.get("price_offered"),
            data.get("status", "pending"),
            created_at
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"]) or dict(data)
