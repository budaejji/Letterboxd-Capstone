import os
import logging
import pandas as pd
import timeit
from src.utils.logging_utils import setup_logger, log_extract_success

# Define the file path for the movies_with_ratings CSV file
FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "raw",
    "unclean_movies_with_ratings.csv",
)

# Configure the logger
logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)

EXPECTED_PERFORMANCE = 0.0001

TYPE = "MOVIES with RATINGS from CSV"


def extract_movies_with_ratings() -> pd.DataFrame:
    start_time = timeit.default_timer()

    try:
        movies_with_ratings = pd.read_csv(FILE_PATH)
        extract_movies_with_ratings_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            TYPE,
            movies_with_ratings.shape,
            extract_movies_with_ratings_execution_time,
            EXPECTED_PERFORMANCE,
        )
        return movies_with_ratings
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")
