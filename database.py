import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "profiles.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS child_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                blood_group TEXT,
                allergies TEXT,
                medical_conditions TEXT,
                medications TEXT,
                emergency_contact TEXT,
                emergency_phone TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()


def create_profile(data: dict) -> int:
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO child_profiles
            (name, age, gender, blood_group, allergies, medical_conditions,
             medications, emergency_contact, emergency_phone, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["age"],
                data["gender"],
                data.get("blood_group", ""),
                data.get("allergies", ""),
                data.get("medical_conditions", ""),
                data.get("medications", ""),
                data.get("emergency_contact", ""),
                data.get("emergency_phone", ""),
                data.get("notes", ""),
                now,
                now,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_profiles():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM child_profiles ORDER BY updated_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_profile(profile_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM child_profiles WHERE id = ?", (profile_id,)
        ).fetchone()
        return dict(row) if row else None


def update_profile(profile_id: int, data: dict):
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE child_profiles SET
                name = ?, age = ?, gender = ?, blood_group = ?,
                allergies = ?, medical_conditions = ?, medications = ?,
                emergency_contact = ?, emergency_phone = ?, notes = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["age"],
                data["gender"],
                data.get("blood_group", ""),
                data.get("allergies", ""),
                data.get("medical_conditions", ""),
                data.get("medications", ""),
                data.get("emergency_contact", ""),
                data.get("emergency_phone", ""),
                data.get("notes", ""),
                now,
                profile_id,
            ),
        )
        conn.commit()


def delete_profile(profile_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM child_profiles WHERE id = ?", (profile_id,))
        conn.commit()
