SELECT DISTINCT
    sender_id AS channel_id,
    channel_name
FROM {{ ref('stg_telegram_messages') }}
WHERE sender_id IS NOT NULL
