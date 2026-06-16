CREATE OR REPLACE TABLE review_delivery_analysis AS
SELECT
    CASE
        WHEN delivery_delay_days IS NULL THEN 'Unknown'
        WHEN delivery_delay_days <= 0 THEN 'On time / Early'
        WHEN delivery_delay_days BETWEEN 1 AND 3 THEN 'Delayed 1-3 days'
        WHEN delivery_delay_days BETWEEN 4 AND 7 THEN 'Delayed 4-7 days'
        ELSE 'Delayed 8+ days'
    END AS delivery_delay_bucket,
    COUNT(DISTINCT order_id) AS orders,
    AVG(review_score) AS avg_review_score,
    SUM(item_gmv) AS gmv
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY avg_review_score;

COPY review_delivery_analysis TO 'data/processed/review_delivery_analysis.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE category_satisfaction AS
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS orders,
    SUM(item_gmv) AS gmv,
    AVG(review_score) AS avg_review_score,
    AVG(delivery_days) AS avg_delivery_days,
    AVG(delivery_delay_days) AS avg_delivery_delay_days
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1
HAVING COUNT(DISTINCT order_id) >= 50
ORDER BY avg_review_score ASC, gmv DESC;

COPY category_satisfaction TO 'data/processed/category_satisfaction.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE state_satisfaction AS
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS orders,
    SUM(item_gmv) AS gmv,
    AVG(review_score) AS avg_review_score,
    AVG(delivery_days) AS avg_delivery_days,
    AVG(delivery_delay_days) AS avg_delivery_delay_days
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY avg_review_score ASC;

COPY state_satisfaction TO 'data/processed/state_satisfaction.csv' (HEADER, DELIMITER ',');
