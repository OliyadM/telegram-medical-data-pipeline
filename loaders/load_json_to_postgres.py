import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

RAW_MSG_PATH = Path("data/raw/telegram_messages")

def connect():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Successfully connected to PostgreSQL.")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        exit(1)

def create_raw_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                    id INTEGER,
                    text TEXT,
                    date TIMESTAMP,
                    has_photo BOOLEAN,
                    sender_id BIGINT,
                    channel_name TEXT,
                    scraped_date DATE
                );
            """)
        conn.commit()
        print("✅ Schema and table ensured.")
    except Exception as e:
        print(f"❌ Error creating schema/table: {e}")
        conn.rollback()

def insert_messages(conn, channel_file, channel_name, scraped_date):
    inserted_count = 0
    try:
        with open(channel_file, "r", encoding="utf-8") as f:
            messages = json.load(f)

        with conn.cursor() as cur:
            for msg in messages:
                try:
                    cur.execute("""
                        INSERT INTO raw.telegram_messages 
                        (id, text, date, has_photo, sender_id, channel_name, scraped_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (
                        msg.get("id"), msg.get("text"), msg.get("date"), msg.get("has_photo"),
                        msg.get("sender_id"), channel_name, scraped_date
                    ))
                    inserted_count += 1
                except Exception as msg_error:
                    print(f"⚠️ Skipped message ID {msg.get('id')} due to error: {msg_error}")
        conn.commit()
        print(f"✅ Inserted {inserted_count} rows for {channel_name} ({scraped_date})")
    except Exception as e:
        print(f"❌ Error loading file {channel_file}: {e}")
        conn.rollback()

def main():
    conn = connect()
    create_raw_table(conn)

    for date_folder in RAW_MSG_PATH.iterdir():
        if not date_folder.is_dir():
            continue
        for json_file in date_folder.glob("*.json"):
            channel_name = json_file.stem
            print(f"📥 Loading {json_file}")
            insert_messages(conn, json_file, channel_name, date_folder.name)

    conn.close()
    print("✅ All messages processed.")

if __name__ == "__main__":
    main()
