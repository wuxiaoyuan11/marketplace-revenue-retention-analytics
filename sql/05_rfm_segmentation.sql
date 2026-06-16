CREATE OR REPLACE TABLE customer_rfm AS
WITH order_level AS (
    SELECT DISTINCT
        customer_unique_id,
        order_id,
        purchase_ts,
        order_payment_value
    FROM order_item_wide
    WHERE order_status = 'delivered'
),
customer_base AS (
    SELECT
        customer_unique_id,
        MAX(purchase_ts) AS last_purchase_ts,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(order_payment_value) AS monetary
    FROM order_level
    GROUP BY 1
),
rfm_score AS (
    SELECT
        *,
        DATE_DIFF('day', last_purchase_ts, (SELECT MAX(purchase_ts) FROM order_level)) AS recency_days,
        NTILE(5) OVER (ORDER BY DATE_DIFF('day', last_purchase_ts, (SELECT MAX(purchase_ts) FROM order_level)) DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency) AS f_score,
        NTILE(5) OVER (ORDER BY monetary) AS m_score
    FROM customer_base
)
SELECT
    customer_unique_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND frequency = 1 THEN 'Potential Loyalists'
        WHEN r_score <= 2 AND (f_score >= 4 OR m_score >= 4) THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Dormant'
        ELSE 'One-time / Mid Value'
    END AS rfm_segment
FROM rfm_score;

COPY customer_rfm TO 'data/processed/customer_rfm.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE rfm_segment_summary AS
SELECT
    rfm_segment,
    COUNT(*) AS customers,
    AVG(recency_days) AS avg_recency_days,
    AVG(frequency) AS avg_frequency,
    AVG(monetary) AS avg_monetary,
    SUM(monetary) AS total_gmv
FROM customer_rfm
GROUP BY 1
ORDER BY total_gmv DESC;

COPY rfm_segment_summary TO 'data/processed/rfm_segment_summary.csv' (HEADER, DELIMITER ',');
