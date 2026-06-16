CREATE OR REPLACE TABLE seller_sla_summary AS
WITH seller_order_level AS (
    SELECT
        w.seller_id,
        s.seller_state,
        w.order_id,
        MAX(w.delivery_delay_days) AS delivery_delay_days,
        AVG(w.review_score) AS review_score,
        SUM(w.item_gmv) AS order_gmv
    FROM order_item_wide w
    LEFT JOIN sellers s
        ON w.seller_id = s.seller_id
    WHERE w.order_status = 'delivered'
      AND w.seller_id IS NOT NULL
    GROUP BY 1, 2, 3
),
seller_metrics AS (
    SELECT
        seller_id,
        seller_state,
        COUNT(DISTINCT order_id) AS delivered_orders,
        SUM(order_gmv) AS gmv,
        AVG(delivery_delay_days) AS avg_delivery_delay_days,
        AVG(review_score) AS avg_review_score,
        AVG(CASE WHEN delivery_delay_days > 0 THEN 1.0 ELSE 0.0 END) AS late_delivery_rate,
        AVG(CASE WHEN delivery_delay_days >= 8 THEN 1.0 ELSE 0.0 END) AS severe_delay_rate,
        AVG(CASE WHEN review_score <= 2 THEN 1.0 ELSE 0.0 END) AS poor_review_rate
    FROM seller_order_level
    GROUP BY 1, 2
)
SELECT
    seller_id,
    seller_state,
    delivered_orders,
    gmv,
    avg_delivery_delay_days,
    avg_review_score,
    late_delivery_rate,
    severe_delay_rate,
    poor_review_rate,
    gmv * (late_delivery_rate + severe_delay_rate + poor_review_rate) AS sla_risk_score
FROM seller_metrics
WHERE delivered_orders >= 50
ORDER BY sla_risk_score DESC;

COPY seller_sla_summary TO 'data/processed/seller_sla_summary.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE category_risk_score AS
WITH category_metrics AS (
    SELECT
        product_category,
        COUNT(DISTINCT order_id) AS orders,
        SUM(item_gmv) AS gmv,
        AVG(review_score) AS avg_review_score,
        AVG(delivery_days) AS avg_delivery_days,
        AVG(CASE WHEN delivery_delay_days > 0 THEN 1.0 ELSE 0.0 END) AS late_delivery_rate,
        AVG(CASE WHEN delivery_delay_days >= 8 THEN 1.0 ELSE 0.0 END) AS severe_delay_rate,
        AVG(CASE WHEN review_score <= 2 THEN 1.0 ELSE 0.0 END) AS poor_review_rate
    FROM order_item_wide
    WHERE order_status = 'delivered'
      AND product_category IS NOT NULL
    GROUP BY 1
),
scored AS (
    SELECT
        *,
        gmv / SUM(gmv) OVER () AS gmv_share,
        GREATEST(4.5 - avg_review_score, 0) / 4.5 AS review_gap_index
    FROM category_metrics
    WHERE orders >= 100
)
SELECT
    product_category,
    orders,
    gmv,
    gmv_share,
    avg_review_score,
    avg_delivery_days,
    late_delivery_rate,
    severe_delay_rate,
    poor_review_rate,
    gmv_share * (review_gap_index + late_delivery_rate + severe_delay_rate + poor_review_rate) AS category_risk_score
FROM scored
ORDER BY category_risk_score DESC;

COPY category_risk_score TO 'data/processed/category_risk_score.csv' (HEADER, DELIMITER ',');

CREATE OR REPLACE TABLE cohort_ltv_proxy AS
WITH order_level AS (
    SELECT DISTINCT
        order_id,
        customer_unique_id,
        DATE_TRUNC('month', purchase_ts) AS order_month,
        order_payment_value
    FROM order_item_wide
    WHERE order_status = 'delivered'
),
customer_cohort AS (
    SELECT
        customer_unique_id,
        MIN(order_month) AS cohort_month
    FROM order_level
    GROUP BY 1
),
cohort_orders AS (
    SELECT
        c.cohort_month,
        DATE_DIFF('month', c.cohort_month, o.order_month) AS month_number,
        o.customer_unique_id,
        o.order_id,
        o.order_payment_value
    FROM order_level o
    JOIN customer_cohort c
        ON o.customer_unique_id = c.customer_unique_id
),
cohort_size AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_unique_id) AS cohort_customers
    FROM customer_cohort
    GROUP BY 1
),
monthly_ltv AS (
    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT customer_unique_id) AS active_customers,
        COUNT(DISTINCT order_id) AS orders,
        SUM(order_payment_value) AS cohort_gmv
    FROM cohort_orders
    GROUP BY 1, 2
)
SELECT
    m.cohort_month,
    m.month_number,
    m.active_customers,
    s.cohort_customers,
    m.orders,
    m.cohort_gmv,
    SUM(m.cohort_gmv) OVER (
        PARTITION BY m.cohort_month
        ORDER BY m.month_number
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_gmv,
    SUM(m.cohort_gmv) OVER (
        PARTITION BY m.cohort_month
        ORDER BY m.month_number
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) / s.cohort_customers AS cumulative_gmv_per_cohort_customer
FROM monthly_ltv m
JOIN cohort_size s
    ON m.cohort_month = s.cohort_month
ORDER BY m.cohort_month, m.month_number;

COPY cohort_ltv_proxy TO 'data/processed/cohort_ltv_proxy.csv' (HEADER, DELIMITER ',');
