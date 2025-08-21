import pandas as pd
from src.utils.file_utils import save_dataframe_to_csv


def clean_movies_with_ratings(
    movies_with_ratings: pd.DataFrame
) -> pd.DataFrame:
    # Task 1 - Drop id column
    movies_with_ratings = drop_id_column(movies_with_ratings)
    # Task 2 - Convert date to integer type
    movies_with_ratings = convert_date_to_int(movies_with_ratings)
    # Task 3 - Convert minute to integer type
    movies_with_ratings = convert_minute_to_int(movies_with_ratings)
    # Task 4 - Standardise ratings
    movies_with_ratings = standardise_ratings(movies_with_ratings)
    # Reset index
    movies_with_ratings.reset_index(drop=True, inplace=True)

    # Save the dataframe as a CSV for logging purposes
    # Ensure the directory exists
    output_dir = "data/processed"
    file_name = "cleaned_movies_with_ratings.csv"
    save_dataframe_to_csv(movies_with_ratings, output_dir, file_name)

    return movies_with_ratings


def convert_date_to_int(movies_with_ratings: pd.DataFrame) -> pd.DataFrame:
    # Convert the date column to a integer format
    movies_with_ratings['date'] = movies_with_ratings['date'].astype('Int64')
    return movies_with_ratings


def convert_minute_to_int(movies_with_ratings: pd.DataFrame) -> pd.DataFrame:
    # Convert the minute column to a integer format
    movies_with_ratings['minute'] = movies_with_ratings['minute'].astype(
        'Int64'
    )
    return movies_with_ratings


def standardise_ratings(movies_with_ratings: pd.DataFrame) -> pd.DataFrame:
    # Multiply ratings by 2 so that they are on a 1-10 scale like the
    # user_ratings
    movies_with_ratings['rating'] = movies_with_ratings['rating'] * 2
    return movies_with_ratings


def drop_id_column(movies_with_ratings: pd.DataFrame) -> pd.DataFrame:
    # Drop the id column
    return movies_with_ratings.drop(columns=["id"])
