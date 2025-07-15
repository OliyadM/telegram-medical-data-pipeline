import json
import psycopg2
from dotenv import load_dotenv
import os

# Load DB credentials
load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
cur = conn.cursor()

# Read detections.json
with open('enrichment/detections.json') as f:
    detections = json.load(f)

insert_query = """
    INSERT INTO enrichment.raw_image_detections (message_id, image_path, detected_class, confidence)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""

for det in detections:
    cur.execute(insert_query, (
        det['message_id'],
        det['image_path'],
        det['detected_class'],
        det['confidence']
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Detection results loaded into PostgreSQL")
