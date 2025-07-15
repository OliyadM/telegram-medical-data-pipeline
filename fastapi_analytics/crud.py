from typing import List
from psycopg2.extras import RealDictCursor
from .database import get_db_connection
from .schemas import TopProduct, ChannelActivity, MessageSearchResult
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_top_products(limit: int = 10) -> List[TopProduct]:
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT LOWER(word) as product_name, COUNT(*) as count
    FROM raw.fct_messages
    CROSS JOIN LATERAL unnest(string_to_array(message_text, ' ')) as word
    WHERE message_text IS NOT NULL
    GROUP BY product_name
    ORDER BY count DESC
    LIMIT %s;
    """
    try:
        logger.debug(f"Executing query get_top_products with limit={limit}")
        cur.execute(query, (limit,))
        results = cur.fetchall()
    except Exception as e:
        logger.error(f"Error in get_top_products: {e}")
        results = []
    finally:
        cur.close()
        conn.close()
    return results


def get_channel_activity(channel_name: str) -> ChannelActivity:
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT 
        channel_name,
        COUNT(*) AS total_messages,
        COUNT(*) FILTER (WHERE has_photo IS TRUE) AS messages_with_images,
        COUNT(*) FILTER (WHERE has_photo IS FALSE) AS messages_with_text_only
    FROM raw.fct_messages
    WHERE channel_name ILIKE %s
    GROUP BY channel_name;
    """
    try:
        logger.debug(f"Executing query get_channel_activity for channel={channel_name}")
        cur.execute(query, (channel_name,))
        result = cur.fetchone()
    except Exception as e:
        logger.error(f"Error in get_channel_activity: {e}")
        result = None
    finally:
        cur.close()
        conn.close()
    return result


def search_messages(query_text: str) -> List[MessageSearchResult]:
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT message_id, message_text, message_date, channel_name
    FROM raw.fct_messages
    WHERE message_text ILIKE %s
    ORDER BY message_date DESC
    LIMIT 20;
    """
    try:
        logger.debug(f"Executing search_messages with query='{query_text}'")
        cur.execute(query, (f"%{query_text}%",))
        results = cur.fetchall()
    except Exception as e:
        logger.error(f"Error in search_messages: {e}")
        results = []
    finally:
        cur.close()
        conn.close()
    return results
