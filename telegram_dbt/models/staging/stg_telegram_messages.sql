

with raw as (

    select * from raw.telegram_messages

)

select
    id,
    text,
    date::timestamp as message_date,
    has_photo::boolean,
    sender_id::bigint,
    channel_name,
    scraped_date::date

from raw


