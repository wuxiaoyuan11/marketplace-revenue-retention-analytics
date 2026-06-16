CREATE OR REPLACE TABLE order_status_funnel AS
SELECT
    order_status,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    COUNT(DISTINCT order_id) * 1.0 / SUM(COUNT(DISTINCT order_id)) OVER () AS order_share
FROM order_item_wide
GROUP BY 1
ORDER BY orders DESC;

COPY order_status_funnel TO 'data/processed/order_status_funnel.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE monthly_order_status AS
SELECT
    DATE_TRUNC('month', purchase_ts) AS month,
    order_status,
    COUNT(DISTINCT order_id) AS orders
FROM order_item_wide
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

COPY monthly_order_status TO 'data/processed/monthly_order_status.csv' (HEADER, DELIMITER ',');

