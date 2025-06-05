import asyncpg
import os
from dotenv import load_dotenv
import csv
load_dotenv()
from animal_shelter_bot.registration.app.utils import normalize_phone

async def get_conn():
    return await asyncpg.connect(
        database='animal_shelter_db',
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host='127.0.0.1',
        port='5432'
    )

async def get_user_role_by_phone(phone: str) -> str | None:
    conn = await get_conn()
    try:
        result = await conn.fetchrow(
            "SELECT role FROM client WHERE number = $1",
            phone
        )
        return result['role'] if result else None
    finally:
        await conn.close()

async def get_user_by_id(user_id: str) -> dict | None:
    conn = await get_conn()
    try:
        row = await conn.fetchrow(
            "SELECT * FROM client WHERE user_id = $1",
            user_id
        )
        if row:
            return {
                "user_id": row['user_id'],
                "name": row['name'],
                "surname": row['surname'],
                "number": row['number'],
                "email": row['email'],
                "age": row['age'],
                "city": row['city'],
                "role": row['role']
            }
        return None
    finally:
        await conn.close()

async def insert_user(data: dict) -> None:
    conn = await get_conn()
    try:
        await conn.execute(
            """
            INSERT INTO client (user_id, name, surname, number, email, age, city, role)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            data['user_id'], data['name'], data['surname'], data['number'],
            data['email'], data['age'], data['city'], 'user'
        )
    finally:
        await conn.close()

async def get_user_by_phone(phone_input: str) -> dict | None:
    """Ищет пользователя по нормализованному номеру телефона"""
    normalized_input = normalize_phone(phone_input)

    conn = await get_conn()
    try:
        rows = await conn.fetch("SELECT * FROM client")
        for row in rows:
            db_number = normalize_phone(row["number"])
            if db_number == normalized_input:
                return {
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "surname": row["surname"],
                    "number": row["number"],
                    "email": row["email"],
                    "age": row["age"],
                    "city": row["city"],
                    "role": row["role"]
                }
        return None
    finally:
        await conn.close()

async def add_new_user(user_id, name, surname, number, email, age, city, role):
    conn = await get_conn()
    try:
        await conn.execute(
            """
            INSERT INTO client (user_id, name, surname, number, email, age, city, role)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            user_id, name, surname, number, email, age, city, role
        )
    finally:
        await conn.close()


async def export_all_users_to_csv(filename: str = "users_export.csv"):
    conn = await get_conn()
    try:
        rows = await conn.fetch("SELECT * FROM client")
        if not rows:
            print("Нет данных для экспорта.")
            return

        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(rows[0].keys())  # заголовки
            for row in rows:
                writer.writerow(row.values())

        print(f" Данные выгружены в {filename}")
    finally:
        await conn.close()

async def update_user_role(phone: str, new_role: str):
    """Обновление роли пользователя по нормализованному номеру"""
    normalized_phone = normalize_phone(phone)

    conn = await get_conn()
    try:
        rows = await conn.fetch("SELECT user_id, number FROM client")
        for row in rows:
            db_phone = normalize_phone(row["number"])
            if db_phone == normalized_phone:
                await conn.execute(
                    "UPDATE client SET role = $1 WHERE user_id = $2",
                    new_role,
                    row["user_id"]
                )
                return True  # успешное обновление
        return False  # пользователь не найден
    finally:
        await conn.close()

async def get_all_admins():
    """Получить всех администраторов"""
    conn = await get_conn()
    try:
        return await conn.fetch(
            "SELECT * FROM client WHERE role = 'admin' ORDER BY name"
        )
    finally:
        await conn.close()

async def search_users(search_term: str):
    """Поиск пользователей"""
    conn = await get_conn()
    try:
        return await conn.fetch(
            "SELECT * FROM client WHERE number LIKE $1 OR name LIKE $1 OR surname LIKE $1",
            f"%{search_term}%"
        )
    finally:
        await conn.close()