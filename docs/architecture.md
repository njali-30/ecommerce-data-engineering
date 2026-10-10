# Pipeline Architecture

## 1. Overview

The E-Commerce Database & Analytics project uses PostgreSQL to store transactional data, Python to orchestrate the pipeline, SQL to perform analytics, and pandas to export reports as CSV files.

## 2. Architecture

```text
PostgreSQL Database
        |
        v
Data Quality Checks
        |
        v
Are all checks passing?
        |
   +----+----+
   |         |
  No        Yes
   |         |
 Stop        v
       Analytics SQL Queries
               |
               v
       pandas DataFrames
               |
               v
        CSV Report Files
               |
               v
            outputs/
```

## 3. Pipeline Workflow

1. **Database connection:** SQLAlchemy establishes a connection to PostgreSQL using the configured database credentials.
2. **Data quality validation:** Python executes four SQL checks to identify missing customer emails, invalid product prices, invalid order quantities, and orders without matching customers.
3. **Failure handling:** If any quality check reports one or more issues, the pipeline stops before exporting analytics reports.
4. **Data extraction:** SQL queries aggregate sales by month, identify top-selling products, and calculate revenue by product category.
5. **Report generation:** pandas converts query results into DataFrames and exports them as CSV files in the `outputs/` directory.

## 4. Technology Stack

- **PostgreSQL:** Relational database management.
- **SQL:** Schema creation, constraints, joins, aggregations, and analytical queries.
- **Python:** Pipeline orchestration and quality-check execution.
- **SQLAlchemy:** Database connectivity.
- **pandas:** Query result handling and CSV generation.
- **pytest:** Automated testing.

## 5. Output Reports

| Report | Purpose |
|---|---|
| `monthly_sales.csv` | Summarizes order counts and gross revenue by month |
| `top_products.csv` | Identifies the top five products by sales |
| `category_revenue.csv` | Summarizes sales quantities and gross revenue by category |

## 6. Reliability and Limitations

The pipeline validates selected data quality rules before generating reports. Database constraints provide additional protection against invalid records.

The current implementation processes data from PostgreSQL and generates batch reports. It does not currently implement streaming, cloud storage, distributed processing, automated scheduling, or incremental data loading.

The quality checks cover selected issues rather than every possible data quality problem. In particular, the database constraints already prevent some invalid records from being inserted through normal database operations.

## 7. Potential Improvements

- Add automated scheduling and workflow orchestration.
- Implement incremental data extraction.
- Expand data quality checks and test failure scenarios.
- Add structured logging and monitoring.
- Introduce cloud storage and distributed processing when required.
