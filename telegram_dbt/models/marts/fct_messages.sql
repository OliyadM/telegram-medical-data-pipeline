WITH raw_messages AS (
    SELECT *
    FROM {{ ref('stg_telegram_messages') }}
    WHERE NOT (text IS NULL AND has_photo = FALSE)
),

messages_with_dims AS (
    SELECT
        rm.id AS message_id,
        rm.sender_id AS channel_id,
        rm.message_date::date AS date_day,
        rm.text AS message_text,
        LENGTH(rm.text) AS message_length,
        rm.has_photo
    FROM raw_messages rm
    INNER JOIN {{ ref('dim_channels') }} dc ON rm.sender_id = dc.channel_id
    INNER JOIN {{ ref('dim_dates') }} dd ON rm.message_date::date = dd.date_day
)

SELECT DISTINCT * FROM messages_with_dims
