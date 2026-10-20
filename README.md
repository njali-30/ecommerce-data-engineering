# E-Commerce Database & Analytics Pipeline

A beginner-friendly Data Engineering project that uses PostgreSQL, Python, Pandas, SQL, and SQLAlchemy to store e-commerce data, validate data quality, and generate analytical reports.

## Project Objectives

- Design a relational database for an e-commerce business.
- Implement primary keys, foreign keys, constraints, and indexes.
- Write SQL queries for sales, product, customer, and category analytics.
- Extract analytical data from PostgreSQL using Python and SQLAlchemy.
- Process query results using Pandas and export them as CSV reports.
- Run data quality checks before generating reports.
- Execute the workflow through a single pipeline entry point.
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

| Category | Technologies |
|---|---|
| Database | PostgreSQL |
| Programming language | Python |
| Data processing | Pandas, NumPy |
| Database connectivity | SQLAlchemy, psycopg |
| Query language | SQL |
| Testing | pytest |
| Configuration | python-dotenv |
| Version control | Git |

## Database Schema

The project uses five relational tables.

| Table | Purpose |
|---|---|
| `customers` | Stores customer details |
| `categories` | Stores product categories |
| `products` | Stores product details, prices, and stock information |
| `orders` | Stores order dates and statuses |
| `order_items` | Stores products and quantities associated with orders |

The schema uses primary keys, foreign keys, uniqueness constraints, validation checks, and indexes to maintain relational integrity and support queries.

## Analytics Reports

The pipeline generates three CSV reports in the `outputs/` directory.

| Report | Purpose |
|---|---|
| `monthly_sales.csv` | Monthly order counts and gross sales |
| `top_products.csv` | Top five products by units sold |
| `category_revenue.csv` | Sales and units sold by product category |

The project also includes SQL queries for customer spending and other sales analytics.

**Metric definition:** Gross sales include order items associated with every non-cancelled order, including pending and confirmed orders. This is an analytical measure for this sample project, not recognized accounting revenue.

## Data Quality Checks

The pipeline validates the following conditions:

- Customers with missing or blank email addresses.
- Products with invalid prices.
- Order items with invalid quantities.
- Orders referencing nonexistent customers.

The combined pipeline is designed to stop before exporting reports when its data quality checks detect issues.

## Project Structure

```text
ecommerce-data-engineering/
├── docs/
│   ├── architecture.md
│   └── data_dictionary.md
├── data/
│   ├── raw/
│   └── processed/
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
│       ├── logging_config.py
│       ├── quality.py
│       └── run_pipeline.py
├── tests/
│   ├── integration/
│   │   └── test_postgres_integration.py
│   ├── test_extract.py
│   ├── test_pipeline.py
│   └── test_quality.py
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

The commands below use PowerShell on Windows.

## Setup and Execution

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

### 3. Install the project and dependencies

Install the project in editable mode with its development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

### 4. Configure database credentials

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your PostgreSQL connection details. Use the variable names defined in `.env.example`.

**Security:** Never commit `.env` or expose database passwords. The `.env` file should remain excluded through `.gitignore`.

### 5. Create and populate the database

Create a PostgreSQL database named `ecommerce` using your PostgreSQL administration tool or the command below:

```powershell
createdb -U postgres -h localhost -p 5432 ecommerce
```

Then initialize the schema and insert the sample data:

```powershell
psql -U postgres -h localhost -p 5432 -d ecommerce -v ON_ERROR_STOP=1 -f .\sql\01_create_tables.sql
psql -U postgres -h localhost -p 5432 -d ecommerce -v ON_ERROR_STOP=1 -f .\sql\02_seed_data.sql
```

The seed script is intended for an empty schema. Do not run it repeatedly against already-populated tables.

Adjust the PostgreSQL username, host, and port if your local configuration differs.

### 6. Run the pipeline

```powershell
python -m ecommerce_pipeline.run_pipeline
```

The pipeline connects to PostgreSQL, runs data quality checks, executes analytics queries, and exports the resulting CSV reports to `outputs/`.

## Testing

The project includes unit tests and PostgreSQL integration tests.

### Run unit tests

With the virtual environment activated, run:

```powershell
Remove-Item Env:RUN_DB_INTEGRATION -ErrorAction SilentlyContinue
python -m pytest -v
```

When `RUN_DB_INTEGRATION` is unset, PostgreSQL integration tests are skipped. The unit tests validate analytics logic, data quality behavior, and pipeline functionality.

### Set up the integration-test database

Integration tests use a separate database named `ecommerce_test` to avoid running against the main `ecommerce` database.

Create the test database **once**:

```powershell
createdb -U postgres -h localhost -p 5432 ecommerce_test
```

Initialize its schema and sample data:

```powershell
psql -U postgres -h localhost -p 5432 -d ecommerce_test -v ON_ERROR_STOP=1 -f .\sql\01_create_tables.sql
psql -U postgres -h localhost -p 5432 -d ecommerce_test -v ON_ERROR_STOP=1 -f .\sql\02_seed_data.sql
```

If `ecommerce_test` already exists and is correctly initialized, do not create it or run the seed script again.

### Run PostgreSQL integration tests

Enable integration tests in the current PowerShell session:

```powershell
$env:RUN_DB_INTEGRATION = "1"
python -m pytest tests/integration/test_postgres_integration.py -v
```

The integration tests verify that:

- The connection targets `ecommerce_test`.
- Database quality checks return the expected results.
- Analytics extraction generates reports with the expected row counts and totals.

The integration tests use a temporary output directory, avoiding overwrites of the project's normal reports.

To run the complete test suite, including integration tests:

```powershell
python -m pytest -v
```

**Important:** Run integration tests only when the configured PostgreSQL credentials can access `ecommerce_test`. The tests explicitly verify the database name before running database checks.

## Current Limitations

- Uses sample e-commerce data rather than a live production source.
- Runs locally against PostgreSQL rather than a cloud data warehouse.
- Requires manual execution; scheduled orchestration is not implemented.
- Does not implement incremental data loading or production-scale monitoring.

## Future Improvements

- Implement incremental data loading.
- Expand automated testing and edge-case coverage.
- Improve operational monitoring and failure diagnostics.
- Add a repeatable database reset and seed workflow.
- Add workflow orchestration and cloud deployment.
- Introduce additional data quality rules and report reconciliation.

## Author

Anjali Chandrabhan Sonawane

GitHub: [njali-30](https://github.com/njali-30)
