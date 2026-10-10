# Data Dictionary

## Overview

The database contains five relational tables representing customers, product categories, products, orders, and order line items.

## 1. customers

Stores customer information.

| Column | Type | Description |
|---|---|---|
| `customer_id` | BIGINT | Primary key; automatically generated |
| `first_name` | VARCHAR(100) | Customer's first name |
| `last_name` | VARCHAR(100) | Customer's last name |
| `email` | VARCHAR(255) | Customer's unique email address |
| `city` | VARCHAR(100) | Customer's city; optional |
| `country` | VARCHAR(100) | Customer's country; optional |
| `created_at` | TIMESTAMPTZ | Record creation timestamp |

## 2. categories

Stores product category information.

| Column | Type | Description |
|---|---|---|
| `category_id` | BIGINT | Primary key; automatically generated |
| `category_name` | VARCHAR(100) | Unique category name |
| `description` | TEXT | Category description; optional |

## 3. products

Stores products available in the store.

| Column | Type | Description |
|---|---|---|
| `product_id` | BIGINT | Primary key; automatically generated |
| `product_name` | VARCHAR(200) | Product name |
| `category_id` | BIGINT | Foreign key referencing `categories.category_id` |
| `price` | NUMERIC(12,2) | Product price; must be non-negative |
| `stock_quantity` | INTEGER | Available stock; must be non-negative |
| `is_active` | BOOLEAN | Indicates whether the product is active |
| `created_at` | TIMESTAMPTZ | Record creation timestamp |

## 4. orders

Stores customer order information.

| Column | Type | Description |
|---|---|---|
| `order_id` | BIGINT | Primary key; automatically generated |
| `customer_id` | BIGINT | Foreign key referencing `customers.customer_id` |
| `order_date` | TIMESTAMPTZ | Date and time of the order |
| `status` | VARCHAR(30) | Order status: pending, confirmed, shipped, delivered, or cancelled |

## 5. order_items

Stores the products and quantities associated with each order.

| Column | Type | Description |
|---|---|---|
| `order_item_id` | BIGINT | Primary key; automatically generated |
| `order_id` | BIGINT | Foreign key referencing `orders.order_id` |
| `product_id` | BIGINT | Foreign key referencing `products.product_id` |
| `quantity` | INTEGER | Number of units; must be greater than zero |
| `unit_price` | NUMERIC(12,2) | Price per unit recorded for the order; must be non-negative |

A unique constraint on `(order_id, product_id)` prevents the same product from appearing more than once in a single order.

## 6. Relationships

- One customer can place multiple orders.
- One category can contain multiple products.
- One order can contain multiple order items.
- One product can appear in multiple order items.
- Each order item belongs to one order and references one product.

## 7. Data Integrity

The schema uses primary keys, foreign keys, `NOT NULL`, `UNIQUE`, and `CHECK` constraints to enforce data integrity.

Indexes are defined on frequently used relationship or filtering columns, including customer IDs, order dates, product IDs, and category IDs.
