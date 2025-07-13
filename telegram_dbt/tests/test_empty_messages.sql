SELECT *
FROM {{ ref('fct_messages') }}
WHERE message_text IS NULL AND has_photo = FALSE
