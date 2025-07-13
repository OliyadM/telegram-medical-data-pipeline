WITH raw_messages AS (
    SELECT *
    FROM {{ ref('stg_telegram_messages') }}
    WHERE NOT (text IS NULL AND has_photo = FALSE)  -- filter out empty messages without photos
)

SELECT DISTINCT
    raw_messages.id AS message_id,
    raw_messages.sender_id AS channel_id,
    raw_messages.message_date::date AS date_day,  -- <-- fix column name here
    raw_messages.text AS message_text,
    LENGTH(raw_messages.text) AS message_length,
    raw_messages.has_photo
FROM raw_messages
WHERE raw_messages.id IS NOT NULL
