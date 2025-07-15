with detections as (
    select *
    from {{ ref('stg_image_detections') }}
),

messages as (
    select *
    from {{ ref('fct_messages') }}
)

select
    d.message_id,
    d.detected_class,
    d.confidence,
    d.detection_timestamp,
    m.channel_id,
    m.date_day as message_date
from detections d
left join messages m
    on d.message_id = m.message_id
where m.message_id is not null  -- ✅ only keep detections with matching messages
