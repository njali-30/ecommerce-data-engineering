
import logging

from ecommerce_pipeline.extract import extract_analytics
from ecommerce_pipeline.logging_config import configure_logging
from ecommerce_pipeline.quality import run_quality_checks


logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    logger.info("Pipeline started")

    logger.info("Step 1: Running data quality checks")
    results = run_quality_checks()

    failed_checks = {
        name: count
        for name, count in results.items()
        if count > 0
    }

    for name, count in results.items():
        if count == 0:
            logger.info("PASS: %s - %d issue(s)", name, count)
        else:
            logger.error("FAIL: %s - %d issue(s)", name, count)

    if failed_checks:
        logger.error("Pipeline stopped: data quality checks failed")
        raise SystemExit(
            "Pipeline stopped: data quality checks failed."
        )

    logger.info("Step 2: Extracting analytics")
    extract_analytics()

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
