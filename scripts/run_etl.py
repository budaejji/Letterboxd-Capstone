import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract_data
from src.transform.transform import transform_data
from src.load.load import load_data_to_db
from src.utils.logging_utils import setup_logger

# Use LOG_BASE_PATH if set (for testing), otherwise use default
log_base_path = os.getenv("LOG_BASE_PATH")
logger = setup_logger(
    "etl_pipeline", "etl_pipeline.log", base_path=log_base_path
)


def main():
    try:
        # Get the argument from the run_etl command and set up the environment
        setup_env(sys.argv)
        env = os.getenv("ENV", "unknown")

        logger.info(f"Starting ETL pipeline in {env} environment")

        logger.info("Beginning data extraction phase")
        extracted_data = extract_data()
        logger.info("Data extraction phase completed")

        logger.info("Beginning the data transformation phase")
        transformed_data = transform_data(extracted_data)
        logger.info("Data transformation phase completed")

        logger.info("Beginning data load phase")
        loaded_data = load_data_to_db(transformed_data)
        logger.info("Data load phase completed")

        logger.info(
                f"ETL pipeline completed successfully in {env} environment"
            )

        return loaded_data

    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
