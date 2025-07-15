import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)

cur = conn.cursor()

cur.execute("""
    CREATE SCHEMA IF NOT EXISTS enrichment;

    CREATE TABLE IF NOT EXISTS enrichment.raw_image_detections (
        message_id INTEGER,
        image_path TEXT,
        detected_class TEXT,
        confidence FLOAT,
        detection_timestamp TIMESTAMP DEFAULT NOW()
    );
""")

conn.commit()
cur.close()
conn.close()

print("✅ Table 'enrichment.raw_image_detections' created successfully.")
