CREATE OR REPLACE TABLE customer_monthly_orders AS
SELECT
    customer_unique_id,
    DATE_TRUNC('month', purchase_ts) AS order_month,
    COUNT(DISTINCT order_id) AS orders
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1, 2;

CREATE OR REPLACE TABLE cohort_retention AS
WITH first_purchase AS (
    SELECT
        customer_unique_id,
        MIN(order_month) AS cohort_month
    FROM customer_monthly_orders
    GROUP BY 1
),
cohort_activity AS (
    SELECT
        f.cohort_month,
        o.order_month,
        DATE_DIFF('month', f.cohort_month, o.order_month) AS month_number,
        COUNT(DISTINCT o.customer_unique_id) AS active_customers
    FROM customer_monthly_orders o
    JOIN first_purchase f
        ON o.customer_unique_id = f.customer_unique_id
    GROUP BY 1, 2, 3
),
cohort_size AS (
    SELECT
        cohort_month,
        active_customers AS cohort_customers
    FROM cohort_activity
    WHERE month_number = 0
)
SELECT
    a.cohort_month,
    a.month_number,
    a.active_customers,
    s.cohort_customers,
    a.active_customers * 1.0 / NULLIF(s.cohort_customers, 0) AS retention_rate
FROM cohort_activity a
JOIN cohort_size s
    ON a.cohort_month = s.cohort_month
ORDER BY 1, 2;

COPY cohort_retention TO 'data/processed/cohort_retention.csv' (HEADER, DELIMITER ',');

