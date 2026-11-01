
import os
import uuid
import re
import sqlite3
import jwt

from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from pwdlib import PasswordHash

from backend.app.database import (
    get_db_connection,
    ArtisanProfileRepository,
    BuyerRepository
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

password_hasher = PasswordHash.recommended()

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "CHANGE_THIS_DEVELOPMENT_SECRET"
)

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


# -------------------------
# Request Models
# -------------------------

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    phone: str
    password: str = Field(min_length=8)
    role: Literal["artisan", "buyer"]


class LoginRequest(BaseModel):
    phone: str
    password: str
    role: Literal["artisan", "buyer"]


# -------------------------
# Helper Functions
# -------------------------

def normalize_phone(phone: str):
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 10:
        digits = "91" + digits

    if len(digits) != 12 or not digits.startswith("91"):
        raise HTTPException(
            status_code=400,
            detail="Enter a valid Indian mobile number."
        )

    return "+" + digits


def create_access_token(user_id: str, role: str):

    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_user_response(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "phone": user["phone"],
        "role": user["role"],
        "region": user["region"]
    }


def auth_response(user):
    token = create_access_token(
        user["id"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": create_user_response(user)
    }


# -------------------------
# SIGN UP
# -------------------------

@router.post("/register", status_code=201)
def register(data: RegisterRequest):

    phone = normalize_phone(data.phone)

    user_id = str(uuid.uuid4())

    password_hash = password_hasher.hash(
        data.password
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE phone = ?",
            (phone,)
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Mobile number is already registered."
            )

        cursor.execute("""
            INSERT INTO users (
                id, name, phone, role, region,
                password_hash, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            data.full_name.strip(),
            phone,
            data.role,
            "",
            password_hash,
            datetime.now().isoformat()
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="Mobile number is already registered."
        )

    finally:
        conn.close()

    # Create role-specific profile

    if data.role == "artisan":
        ArtisanProfileRepository.save({
            "id": f"prof-{user_id}",
            "user_id": user_id,
            "artisan_name": data.full_name.strip(),
            "craft_type": "Not specified",
            "location": "India",
            "phone": phone
        })

    else:
        BuyerRepository.save({
            "id": f"buyer-{user_id}",
            "user_id": user_id,
            "buyer_name": data.full_name.strip(),
            "organization": "",
            "buyer_type": "B2B",
            "contact_email": ""
        })

    user = {
        "id": user_id,
        "name": data.full_name.strip(),
        "phone": phone,
        "role": data.role,
        "region": ""
    }

    return auth_response(user)


# -------------------------
# LOGIN
# -------------------------

@router.post("/login")
def login(data: LoginRequest):

    phone = normalize_phone(data.phone)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE phone = ?",
        (phone,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid mobile number or password."
        )

    user = dict(user)

    if not user.get("password_hash"):
        raise HTTPException(
            status_code=401,
            detail="Please create an account with a password first."
        )

    if not password_hasher.verify(
        data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid mobile number or password."
        )

    if user["role"] != data.role:
        raise HTTPException(
            status_code=403,
            detail="Please select the correct account type."
        )

    return auth_response(user)
