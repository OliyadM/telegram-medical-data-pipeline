SELECT *
FROM {{ ref('stg_telegram_messages') }}
WHERE id IS NOT NULL
LIMIT 2
