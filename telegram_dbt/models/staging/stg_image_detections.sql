with raw as (
    select
        message_id,
        image_path,
        detected_class,
        confidence,
        detection_timestamp
    from {{ source('enrichment', 'raw_image_detections') }}
)

select * from raw
