import pandas as pd
from src.extract.extract_movies import extract_movies
from src.extract.extract_movies_with_ratings import extract_movies_with_ratings
from src.extract.extract_user_ratings import extract_user_ratings
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data", "extract_data.log")


def extract_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting data extraction process")

        movies = extract_movies()
        movies_with_ratings = extract_movies_with_ratings()
        user_ratings = extract_user_ratings()

        logger.info(
            f"Data extraction completed successfully - "
            f"Movies: {movies.shape}, Movies with Ratings: "
            f"{movies_with_ratings.shape}, "
            f"User Ratings: {user_ratings.shape}"
        )

        return (movies, movies_with_ratings, user_ratings)

    except Exception as e:
        logger.error(f"Data extraction failed: {str(e)}")
        raise
