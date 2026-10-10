# E-Commerce Database & Analytics Pipeline

A beginner-friendly Data Engineering project that uses PostgreSQL, Python, Pandas, and SQL to store e-commerce data, validate data quality, and generate analytical reports.

## Project Objectives

- Design a relational database for an e-commerce business.
- Implement primary keys, foreign keys, constraints, and indexes.
- Write SQL queries for sales, product, customer, and category analytics.
- Extract query results from PostgreSQL using Python and SQLAlchemy.
- Export analytical datasets as CSV files.
- Run data quality checks before generating reports.
- Automate the workflow through a single pipeline entry point.

## Architecture

```text
Sample E-Commerce Data
          |
          v
    PostgreSQL
 (5 relational tables)
          |
          v
  Data Quality Checks
          |
          v
  Python + SQLAlchemy
          |
          v
   SQL Analytics Queries
          |
          v
     Pandas DataFrames
          |
          v
      CSV Reports
```

## Technology Stack

- **Database:** PostgreSQL
- **Programming:** Python
- **Data processing:** Pandas
- **Database connectivity:** SQLAlchemy, psycopg
- **Query language:** SQL
- **Testing:** pytest
- **Configuration:** python-dotenv
- **Version control:** Git

## Database Schema

| Table | Purpose |
|---|---|
| `customers` | Customer details |
| `categories` | Product categories |
| `products` | Product details, prices, and stock |
| `orders` | Order dates and statuses |
| `order_items` | Products and quantities within orders |

The schema uses primary keys, foreign keys, uniqueness constraints, validation checks, and indexes.

## Analytics Reports

The pipeline generates three CSV reports:

| Report | Purpose |
|---|---|
| `monthly_sales.csv` | Monthly order counts and gross sales |
| `top_products.csv` | Top five products by units sold |
| `category_revenue.csv` | Sales and units sold by category |

The project also includes SQL queries for customer spending and total sales.

**Metric definition:** Gross sales include order items associated with every non-cancelled order, including pending and confirmed orders. This is an analytical measure for this sample project, not recognized accounting revenue.

## Data Quality Checks

The pipeline checks for:

- Customers with missing or blank email addresses.
- Products with invalid prices.
- Order items with invalid quantities.
- Orders referencing nonexistent customers.

If a check detects an issue, the combined pipeline stops before exporting reports.

## Project Structure

```text
ecommerce-data-engineering/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── outputs/
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_seed_data.sql
│   └── 03_analytics.sql
├── src/
│   └── ecommerce_pipeline/
│       ├── __init__.py
│       ├── config.py
│       ├── db.py
│       ├── extract.py
│       ├── quality.py
│       └── run_pipeline.py
├── tests/
│   └── test_extract.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.11 or later
- PostgreSQL
- Git

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/njali-30/ecommerce-data-engineering.git
cd ecommerce-data-engineering
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure database credentials

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your PostgreSQL credentials. Never commit this file or share its password.

### 5. Create and populate the database

Create a PostgreSQL database named `ecommerce`, then run these commands from the project root:

```powershell
psql -U postgres -h localhost -p 5432 -d ecommerce -v ON_ERROR_STOP=1 -f .\sql\01_create_tables.sql
psql -U postgres -h localhost -p 5432 -d ecommerce -v ON_ERROR_STOP=1 -f .\sql\02_seed_data.sql
```

The seed script is intended for an empty schema. Do not run it repeatedly against already-populated tables.

### 6. Run the pipeline

In PowerShell:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m ecommerce_pipeline.run_pipeline
```

Successful execution runs the quality checks and exports the CSV reports to `outputs/`.

### 7. Run tests

```powershell
python -m pytest -v
```

Run the pipeline before the tests because the current tests validate the generated CSV files.

## Current Limitations

- Uses sample e-commerce data rather than a live production source.
- Runs locally against PostgreSQL rather than a cloud warehouse.
- Executes the pipeline manually; scheduled orchestration is not implemented.
- Tests currently validate generated output files rather than testing every database operation independently.

## Future Improvements

- Add incremental data loading.
- Add more comprehensive automated tests.
- Add structured logging and exception handling.
- Add a repeatable database reset and seed workflow.
- Add orchestration and cloud deployment.
- Add more data quality rules and report reconciliation.

## Author

Anjali Chandrabhan Sonawane

GitHub: [njali-30](https://github.com/njali-30)
