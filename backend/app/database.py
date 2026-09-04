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
        price_offered REAL,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


class ProductRepository:
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        if d.get("tags"):
            try:
                d["tags"] = json.loads(d["tags"])
            except Exception:
                d["tags"] = [t.strip() for t in d["tags"].split(",") if t.strip()]
        else:
            d["tags"] = []
        return d

    @classmethod
    def get_all(cls, category: Optional[str] = None, artisan_id: Optional[str] = None, query: Optional[str] = None) -> List[Dict[str, Any]]:
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
            artisan_id, artisan_name, location, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            location=excluded.location
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
            created_at
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])

    @classmethod
    def delete(cls, product_id: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        count = cursor.rowcount
        conn.commit()
        conn.close()
        return count > 0


class UserRepository:
    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = data.get("created_at") or datetime.now().isoformat()
        cursor.execute("""
        INSERT INTO users (id, name, phone, role, region, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            phone=excluded.phone,
            role=excluded.role,
            region=excluded.region
        """, (
            data["id"],
            data["name"],
            data.get("phone", ""),
            data.get("role", "artisan"),
            data.get("region", ""),
            created_at
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])

    @classmethod
    def get_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


class ArtisanProfileRepository:
    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO artisan_profiles (id, user_id, artisan_name, craft_type, location, bio, phone, story_style)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            user_id=excluded.user_id,
            artisan_name=excluded.artisan_name,
            craft_type=excluded.craft_type,
            location=excluded.location,
            bio=excluded.bio,
            phone=excluded.phone,
            story_style=excluded.story_style
        """, (
            data["id"],
            data.get("user_id", data["id"]),
            data["artisan_name"],
            data.get("craft_type", "General Craft"),
            data.get("location", "India"),
            data.get("bio", ""),
            data.get("phone", ""),
            data.get("story_style", "Cultural Heritage")
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])

    @classmethod
    def get_by_id(cls, profile_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artisan_profiles WHERE id = ? OR user_id = ?", (profile_id, profile_id))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


class BuyerRepository:
    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO buyers (id, user_id, buyer_name, organization, buyer_type, contact_email)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            user_id=excluded.user_id,
            buyer_name=excluded.buyer_name,
            organization=excluded.organization,
            buyer_type=excluded.buyer_type,
            contact_email=excluded.contact_email
        """, (
            data["id"],
            data.get("user_id", data["id"]),
            data["buyer_name"],
            data.get("organization", ""),
            data.get("buyer_type", "B2B"),
            data.get("contact_email", "")
        ))
        conn.commit()
        conn.close()
        return cls.get_by_id(data["id"])

    @classmethod
    def get_by_id(cls, buyer_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buyers WHERE id = ? OR user_id = ?", (buyer_id, buyer_id))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


class OrderRepository:
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
        return [dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, order_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @classmethod
    def save(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = data.get("created_at") or datetime.now().isoformat()
        data["created_at"] = created_at
        cursor.execute("""
        INSERT INTO orders (
            id, product_id, product_title, artisan_id, buyer_name, buyer_contact,
            quantity, notes, price_offered, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            status=excluded.status,
            notes=excluded.notes,
            price_offered=excluded.price_offered
        """, (
            data["id"],
            data["product_id"],
            data.get("product_title", ""),
            data.get("artisan_id", ""),
            data["buyer_name"],
            data["buyer_contact"],
            data["quantity"],
            data.get("notes"),
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
        conn.commit()
        conn.close()
        return cls.get_by_id(order_id)

