
from ecommerce_pipeline.extract import extract_analytics
from ecommerce_pipeline.quality import run_quality_checks


def main() -> None:
    print("Step 1: Running data quality checks...")
    results = run_quality_checks()

    failed_checks = {
        name: count
        for name, count in results.items()
        if count > 0
    }

    for name, count in results.items():
        status = "PASS" if count == 0 else "FAIL"
        print(f"{status}: {name} - {count} issue(s)")

    if failed_checks:
        raise SystemExit(
            "Pipeline stopped: data quality checks failed."
        )

    print("\nStep 2: Extracting analytics...")
    extract_analytics()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
