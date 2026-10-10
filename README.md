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
- Test analytics logic and database integration using pytest.

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
- **Data processing:** Pandas, NumPy
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

The pipeline generates three CSV reports in the `outputs/` directory.

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
├── docs/
│   ├── architecture.md
│   └── data_dictionary.md
├── outputs/
│   ├── monthly_sales.csv
│   ├── top_products.csv
│   └── category_revenue.csv
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
│   ├── integration/
│   │   └── test_postgres_integration.py
│   ├── test_extract.py
│   ├── test_pipeline.py
│   └── test_quality.py
├── data/
│   ├── raw/
│   └── processed/
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

```powershell
git clone https://github.com/njali-30/ecommerce-data-engineering.git
cd ecommerce-data-engineering
```

### 2. Create and activate a virtual environment

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

### 5. Create and populate the main database

Create a PostgreSQL database named `ecommerce`. Then run these commands from the project root:

```powershell
psql -U postgres -h localhost -p 5432 -d ecommerce -v ON_ERROR_STOP=1 -f .\sql\01_create_tables.sql
psql -U postgres -h localhost -p 5432 -d ecommerce -v ON_ERROR_STOP=1 -f .\sql\02_seed_data.sql
```

The seed script is intended for an empty schema. Do not run it repeatedly against already-populated tables.

### 6. Run the pipeline

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m ecommerce_pipeline.run_pipeline
```

Successful execution runs the quality checks and exports the CSV reports to `outputs/`.

## Testing

The project includes unit tests and PostgreSQL integration tests.

### Run unit tests

With the virtual environment activated, run:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
Remove-Item Env:RUN_DB_INTEGRATION -ErrorAction SilentlyContinue
python -m pytest -v
```

With `RUN_DB_INTEGRATION` unset, the PostgreSQL integration tests are skipped. The unit tests validate analytics logic, expected report results, and pipeline behavior.

### Set up the integration-test database

Integration tests use a separate database named `ecommerce_test` so they do not run against the main `ecommerce` database.

Create the test database once:

```powershell
psql -U postgres -h localhost -p 5432 -d postgres -c "CREATE DATABASE ecommerce_test;"
```

Initialize its schema and sample data:

```powershell
psql -U postgres -h localhost -p 5432 -d ecommerce_test -v ON_ERROR_STOP=1 -f .\sql\01_create_tables.sql
psql -U postgres -h localhost -p 5432 -d ecommerce_test -v ON_ERROR_STOP=1 -f .\sql\02_seed_data.sql
```

If `ecommerce_test` already exists and is correctly initialized, do not create or seed it again.

### Run PostgreSQL integration tests

Enable integration tests in the current PowerShell session:

```powershell
$env:RUN_DB_INTEGRATION = "1"
python -m pytest tests/integration/test_postgres_integration.py -v
```

The integration tests verify that:

- The connection targets `ecommerce_test`.
- Real database quality checks pass.
- Analytics extraction produces the expected reports and totals.

The tests direct their CSV output to a temporary directory instead of overwriting the project's normal reports.

Run the complete suite with integration tests enabled:

```powershell
python -m pytest -v
```

**Important:** Only enable integration tests when the configured PostgreSQL credentials can access `ecommerce_test`. The tests explicitly verify the database name before running database checks.

## Current Limitations

- Uses sample e-commerce data rather than a live production source.
- Runs locally against PostgreSQL rather than a cloud warehouse.
- Executes the pipeline manually; scheduled orchestration is not implemented.
- Does not yet implement incremental data loading or production-scale monitoring.

## Future Improvements

- Add incremental data loading.
- Expand automated testing and edge-case coverage.
- Add structured logging and exception handling.
- Add a repeatable database reset and seed workflow.
- Add orchestration and cloud deployment.
- Add more data quality rules and report reconciliation.

## Author

Anjali Chandrabhan Sonawane

GitHub: [njali-30](https://github.com/njali-30)
