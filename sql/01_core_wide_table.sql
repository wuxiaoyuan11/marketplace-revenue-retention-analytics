CREATE OR REPLACE TABLE order_item_wide AS
WITH payment_agg AS (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment_value,
        MAX(payment_installments) AS max_payment_installments,
        STRING_AGG(DISTINCT payment_type, ', ') AS payment_types
    FROM order_payments
    GROUP BY 1
),
review_agg AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM order_reviews
    GROUP BY 1
)
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    o.order_status,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchase_ts,
    CAST(o.order_approved_at AS TIMESTAMP) AS approved_ts,
    CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS carrier_ts,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_ts,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_ts,
    oi.order_item_id,
    oi.product_id,
    p.product_category_name,
    COALESCE(t.product_category_name_english, p.product_category_name) AS product_category,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value AS item_gmv,
    pay.payment_types,
    pay.max_payment_installments,
    pay.order_payment_value,
    r.review_score,
    DATE_DIFF('day', CAST(o.order_purchase_timestamp AS TIMESTAMP), CAST(o.order_delivered_customer_date AS TIMESTAMP)) AS delivery_days,
    DATE_DIFF('day', CAST(o.order_estimated_delivery_date AS TIMESTAMP), CAST(o.order_delivered_customer_date AS TIMESTAMP)) AS delivery_delay_days
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation t
    ON p.product_category_name = t.product_category_name
LEFT JOIN payment_agg pay
    ON o.order_id = pay.order_id
LEFT JOIN review_agg r
    ON o.order_id = r.order_id;

COPY order_item_wide TO 'data/processed/order_item_wide.csv' (HEADER, DELIMITER ',');
