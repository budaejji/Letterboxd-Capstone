import pandas as pd
from src.transform.clean_movies import clean_movies
from src.transform.clean_movies_with_ratings import clean_movies_with_ratings
from src.transform.clean_user_ratings import clean_user_ratings
from src.transform.merge_movies_movies_with_ratings import (
    merge_movies_and_movies_with_ratings
)
from src.transform.enrich_merged_with_user_ratings import (
    enrich_movies_table_with_user_ratings_data
)
from src.transform.aggregate_user_ratings import (
    aggregate_user_ratings
)
from src.utils.logging_utils import setup_logger

logger = setup_logger("transform_data", "transform_data.log")


def transform_data(data) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting data transformation process...")
        # Clean movies data
        logger.info("Cleaning movies data...")
        cleaned_movies = clean_movies(data[0])
        logger.info("Movies data cleaned successfully.")
        # Clean movies with ratings data
        logger.info("Cleaning movies with ratings data...")
        cleaned_movies_with_ratings = clean_movies_with_ratings(data[1])
        logger.info("Movies with ratings data cleaned successfully.")
        # Clean user ratings data
        logger.info("Cleaning user ratings data...")
        cleaned_user_ratings = clean_user_ratings(data[2])
        logger.info("User ratings data cleaned successfully.")
        # Enrich movies with ratings data
        logger.info("Merging movies and movies_with_ratings data...")
        merged_data = merge_movies_and_movies_with_ratings(
            cleaned_movies, cleaned_movies_with_ratings
        )
        logger.info("Data merged successfully.")
        # Enrich the merged data with user ratings data
        logger.info("Enriching merged data with user ratings data...")
        enriched_movies_data = enrich_movies_table_with_user_ratings_data(
            merged_data, cleaned_user_ratings
        )
        logger.info(
            "Merged data with user ratings data enriched successfully."
        )
        # Aggregate user ratings data to a new table
        logger.info("Aggregating user ratings data...")
        aggregated_user_ratings = aggregate_user_ratings(cleaned_user_ratings)
        logger.info("User ratings data aggregated successfully.")

        return (
            enriched_movies_data, cleaned_user_ratings, aggregated_user_ratings
        )
    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise
