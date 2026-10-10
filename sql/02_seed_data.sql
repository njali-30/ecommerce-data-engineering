-- =========================================================
-- E-Commerce Database & Analytics
-- File: 02_seed_data.sql
-- Purpose: Insert reproducible sample data
-- =========================================================

BEGIN;

INSERT INTO customers
    (first_name, last_name, email, city, country)
VALUES
    ('Ananya', 'Sharma', 'ananya.sharma@example.com', 'Mumbai', 'India'),
    ('Rohan', 'Patel', 'rohan.patel@example.com', 'Pune', 'India'),
    ('Meera', 'Iyer', 'meera.iyer@example.com', 'Bengaluru', 'India'),
    ('Arjun', 'Desai', 'arjun.desai@example.com', 'Ahmedabad', 'India'),
    ('Sara', 'Khan', 'sara.khan@example.com', 'Hyderabad', 'India'),
    ('Kabir', 'Mehta', 'kabir.mehta@example.com', 'Delhi', 'India'),
    ('Priya', 'Nair', 'priya.nair@example.com', 'Kochi', 'India'),
    ('Ishaan', 'Rao', 'ishaan.rao@example.com', 'Chennai', 'India');

INSERT INTO categories (category_name, description)
VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Home & Kitchen', 'Products for home and kitchen'),
    ('Books', 'Books and learning materials'),
    ('Clothing', 'Clothing and fashion products');

INSERT INTO products
    (product_name, category_id, price, stock_quantity)
VALUES
    ('Wireless Headphones', 1, 2499.00, 40),
    ('USB-C Charger', 1, 899.00, 75),
    ('Bluetooth Speaker', 1, 1799.00, 25),
    ('Coffee Maker', 2, 3299.00, 15),
    ('Water Bottle', 2, 499.00, 100),
    ('SQL for Beginners', 3, 650.00, 60),
    ('Python Programming', 3, 799.00, 45),
    ('Cotton T-Shirt', 4, 599.00, 80),
    ('Running Shoes', 4, 2199.00, 30);

-- Explicit dates make the dataset consistent across reruns.
INSERT INTO orders (customer_id, order_date, status)
VALUES
    (1, '2026-01-05 10:00:00+05:30', 'delivered'),
    (2, '2026-01-12 14:30:00+05:30', 'delivered'),
    (3, '2026-02-03 09:15:00+05:30', 'delivered'),
    (1, '2026-02-18 17:45:00+05:30', 'shipped'),
    (4, '2026-03-02 11:20:00+05:30', 'delivered'),
    (5, '2026-03-15 16:00:00+05:30', 'cancelled'),
    (6, '2026-04-07 12:10:00+05:30', 'delivered'),
    (7, '2026-04-21 18:30:00+05:30', 'confirmed'),
    (8, '2026-05-10 13:00:00+05:30', 'delivered'),
    (2, '2026-05-25 15:40:00+05:30', 'delivered'),
    (3, '2026-06-08 10:50:00+05:30', 'pending'),
    (5, '2026-06-19 19:15:00+05:30', 'delivered');

-- unit_price records the price charged at order time.
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
    (1, 1, 1, 2499.00),
    (1, 6, 2, 650.00),
    (2, 2, 2, 899.00),
    (2, 5, 1, 499.00),
    (3, 4, 1, 3299.00),
    (3, 7, 1, 799.00),
    (4, 3, 1, 1799.00),
    (4, 8, 2, 599.00),
    (5, 9, 1, 2199.00),
    (5, 2, 1, 899.00),
    (6, 1, 1, 2499.00),
    (7, 4, 1, 3299.00),
    (7, 5, 2, 499.00),
    (8, 6, 1, 650.00),
    (8, 8, 1, 599.00),
    (9, 1, 2, 2499.00),
    (9, 3, 1, 1799.00),
    (10, 7, 2, 799.00),
    (10, 5, 3, 499.00),
    (11, 2, 1, 899.00),
    (11, 6, 1, 650.00),
    (12, 9, 1, 2199.00),
    (12, 8, 2, 599.00);

COMMIT;