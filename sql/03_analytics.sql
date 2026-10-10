-- 1. Total revenue from non-cancelled orders
SELECT
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.status <> 'cancelled';

-- 2. Monthly sales summary
SELECT
    DATE_TRUNC('month', o.order_date)::DATE AS sales_month,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.status <> 'cancelled'
GROUP BY DATE_TRUNC('month', o.order_date)::DATE
ORDER BY sales_month;


-- 3. Best-selling products by quantity
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_sales
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.status <> 'cancelled'
GROUP BY p.product_id, p.product_name
ORDER BY units_sold DESC, gross_sales DESC
LIMIT 5;


-- 4. Customer spending summary
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spending
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.status <> 'cancelled'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spending DESC;


-- 5. Revenue by product category
SELECT
    cat.category_name,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue
FROM categories AS cat
JOIN products AS p
    ON cat.category_id = p.category_id
JOIN order_items AS oi
    ON p.product_id = oi.product_id
JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.status <> 'cancelled'
GROUP BY cat.category_id, cat.category_name
ORDER BY gross_revenue DESC;