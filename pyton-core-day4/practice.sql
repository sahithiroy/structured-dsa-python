comment:Find duplicate records based on (device_id, timestamp) and keep only the latest one.

WITH cte_sensorlogs AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY device_id, timestamp
               ORDER BY id DESC
           ) AS latest_readings
    FROM sensor_logs
)
SELECT *
FROM cte_sensorlogs
WHERE latest_readings = 1;

comment:Each inverter produces energy every day. You want the top 2 days with highest energy for each inverter.

with cte_inveter as(
    select *, DENSE_RANK()() OVER(PARTITION by inverter_id order by 
energy_kwh desc)as latest_inverter
from  energy_data
)
select * from cte_inveter  where latest_inverter<=2;


comment: Calculate running total of energy ordered by date.

WITH cte_energy AS (
    SELECT
        date,
        energy_kwh,
        SUM(energy_kwh) OVER (
            ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total_energy
    FROM daily_energy
)
SELECT *
FROM cte_energy;

comment:You want to detect sudden drops in solar production. we have to calaculate today energy and yesterday energy their difference

WITH daily_energy AS (
    SELECT
        date,
        SUM(energy_kwh) AS today_energy
    FROM output_energy
    GROUP BY date
),
energy_comparison AS (
    SELECT
        date,
        today_energy,
        LAG(today_energy) OVER (ORDER BY date) AS yesterday_energy
    FROM daily_energy
)
SELECT
    date,
    today_energy,
    yesterday_energy,
    today_energy - yesterday_energy AS diff_energy
FROM energy_comparison;


comment:Your inverter data has missing dates. You want a continuous date series.

WITH RECURSIVE DateSeries AS (
    SELECT DATE '2024-01-01' AS generated_date
    UNION ALL
    SELECT generated_date + INTERVAL '1 day'
    FROM DateSeries
    WHERE generated_date < DATE '2024-01-10'
)
SELECT generated_date
FROM DateSeries;

comment:Identify missing 15-minute intervals for each device.
WITH ordered_data AS (
    SELECT
        device_id,
        timestamp,
        LAG(timestamp) OVER (
            PARTITION BY device_id
            ORDER BY timestamp
        ) AS prev_timestamp
    FROM iot_data
)
SELECT
    device_id,
    prev_timestamp AS gap_start,
    timestamp       AS gap_end,
    TIMESTAMPDIFF(MINUTE, prev_timestamp, timestamp) AS gap_minutes
FROM ordered_data
WHERE prev_timestamp IS NOT NULL
  AND TIMESTAMPDIFF(MINUTE, prev_timestamp, timestamp) > 15;


comment:Daily energy per inverter

Monthly average from daily data

WITH daily_energy AS (
    SELECT
        inverter_id,
        DATE(timestamp) AS day,
        SUM(energy) AS daily_energy
    FROM raw_energy
    GROUP BY inverter_id, DATE(timestamp)
),
monthly_avg AS (
    SELECT
        inverter_id,
        DATE_FORMAT(day, '%Y-%m') AS month,
        AVG(daily_energy) AS avg_daily_energy
    FROM daily_energy
    GROUP BY inverter_id, DATE_FORMAT(day, '%Y-%m')
)
SELECT *
FROM monthly_avg;


comment:Inverters whose average daily energy > 50 kWh
WITH daily_energy AS (
    SELECT
        inverter_id,
        DATE(timestamp) AS day,
        SUM(energy) AS daily_energy
    FROM raw_energy
    GROUP BY inverter_id, DATE(timestamp)
),
avg_energy AS (
    SELECT
        inverter_id,
        AVG(daily_energy) AS avg_daily_energy
    FROM daily_energy
    GROUP BY inverter_id
)
SELECT *
FROM avg_energy
WHERE avg_daily_energy > 50;