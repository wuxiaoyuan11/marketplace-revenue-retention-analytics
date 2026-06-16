CREATE OR REPLACE TABLE monthly_revenue AS
WITH order_level AS (
    SELECT DISTINCT
        order_id,
        customer_unique_id,
        DATE_TRUNC('month', purchase_ts) AS month,
        order_payment_value,
        review_score
    FROM order_item_wide
    WHERE order_status = 'delivered'
)
SELECT
    month,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    SUM(order_payment_value) AS gmv,
    SUM(order_payment_value) / NULLIF(COUNT(DISTINCT order_id), 0) AS aov,
    AVG(review_score) AS avg_review_score
FROM order_level
GROUP BY 1
ORDER BY 1;

COPY monthly_revenue TO 'data/processed/monthly_revenue.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE category_revenue AS
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    SUM(item_gmv) AS gmv,
    SUM(item_gmv) / NULLIF(COUNT(DISTINCT order_id), 0) AS aov,
    AVG(review_score) AS avg_review_score
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1
HAVING COUNT(DISTINCT order_id) >= 50
ORDER BY gmv DESC;

COPY category_revenue TO 'data/processed/category_revenue.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE state_revenue AS
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    SUM(item_gmv) AS gmv,
    SUM(item_gmv) / NULLIF(COUNT(DISTINCT order_id), 0) AS aov,
    AVG(delivery_days) AS avg_delivery_days,
    AVG(review_score) AS avg_review_score
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY gmv DESC;

COPY state_revenue TO 'data/processed/state_revenue.csv' (HEADER, DELIMITER ',');
