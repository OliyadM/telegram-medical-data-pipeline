-- models/marts/dim_dates.sql
WITH date_range AS (
    SELECT generate_series(
        '2023-01-01'::date,
        CURRENT_DATE,
        interval '1 day'
    ) AS date_day
)

SELECT 
    date_day,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(DOW FROM date_day) AS day_of_week
FROM date_range
