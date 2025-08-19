import pandas as pd
from src.load.load_movies import load_movies
from src.load.load_user_ratings import load_user_ratings
from src.load.load_aggregated_user_ratings import load_aggregated_user_ratings
from src.utils.logging_utils import setup_logger

logger = setup_logger("load_data", "load_data.log")


def load_data_to_db(data) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting loading process")
        # Load enriched movies DataFrame into database
        logger.info("Loading movies data...")
        loaded_movies = load_movies(data[0])
        logger.info("Movies data loaded successfully.")
        # Load cleaned user ratings DataFrame into database
        logger.info("Loading user ratings data...")
        loaded_user_ratings = load_user_ratings(data[1])
        logger.info("User ratings data loaded successfully.")
        # Load aggregated user ratings DataFrame into database
        logger.info("Loading aggregated user ratings data...")
        loaded_aggregated_user_ratings = load_aggregated_user_ratings(data[2])
        logger.info("Aggregated user ratings data loaded successfully.")

        logger.info(
            f"Data loading completed successfully - "
            f"Movies: {loaded_movies.shape}, "
            f"User Ratings: {loaded_user_ratings.shape}, "
            f"Aggregated User Ratings: {loaded_aggregated_user_ratings.shape}"
        )

        return (
            loaded_movies, loaded_user_ratings, loaded_aggregated_user_ratings
        )

    except Exception as e:
        logger.error(f"Data loading failed: {str(e)}")
        raise
