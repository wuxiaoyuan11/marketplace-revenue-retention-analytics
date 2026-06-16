-- Use these as interview talking points.

-- 1. Top 10 categories by GMV
SELECT
    product_category,
    SUM(item_gmv) AS gmv,
    COUNT(DISTINCT order_id) AS orders,
    SUM(item_gmv) / COUNT(DISTINCT order_id) AS aov
FROM order_item_wide
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY gmv DESC
LIMIT 10;

-- 2. Monthly repeat customer rate
WITH monthly_customer_orders AS (
    SELECT
        DATE_TRUNC('month', purchase_ts) AS month,
        customer_unique_id,
        COUNT(DISTINCT order_id) AS monthly_orders
    FROM order_item_wide
    WHERE order_status = 'delivered'
    GROUP BY 1, 2
)
SELECT
    month,
    COUNT(*) AS customers,
    SUM(CASE WHEN monthly_orders > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    SUM(CASE WHEN monthly_orders > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS repeat_customer_rate
FROM monthly_customer_orders
GROUP BY 1
ORDER BY 1;

-- 3. Revenue at risk from delayed deliveries
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS delayed_orders,
    SUM(item_gmv) AS delayed_gmv,
    AVG(review_score) AS avg_review_score
FROM order_item_wide
WHERE order_status = 'delivered'
  AND delivery_delay_days > 0
GROUP BY 1
ORDER BY delayed_gmv DESC;
