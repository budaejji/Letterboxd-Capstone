import pandas as pd
from src.utils.file_utils import save_dataframe_to_csv


def clean_user_ratings(user_ratings: pd.DataFrame) -> pd.DataFrame:
    # Task 1 - Remove rows with missing data
    cleaned_user_ratings = remove_missing_values(user_ratings)
    # Task 2 - Anonymise user_id
    cleaned_user_ratings = anonymise_user_id(cleaned_user_ratings)
    # Task 3 - Consolidate duplicated movies
    cleaned_user_ratings = consolidate_duplicated_movies(cleaned_user_ratings)
    # Task 4 - Remove duplicate rows
    cleaned_user_ratings = cleaned_user_ratings.drop_duplicates()
    # Task 5 - Consolidate ratings for same movie rated differently by a user
    cleaned_user_ratings = consolidate_ratings_for_same_movie(
        cleaned_user_ratings
    )
    # Reset index
    cleaned_user_ratings.reset_index(drop=True, inplace=True)

    # Save the dataframe as a CSV for logging purposes
    # Ensure the directory exists
    output_dir = "data/processed"
    file_name = "cleaned_user_ratings.csv"
    save_dataframe_to_csv(cleaned_user_ratings, output_dir, file_name)

    return cleaned_user_ratings


def remove_missing_values(user_ratings: pd.DataFrame) -> pd.DataFrame:
    # Remove rows with missing values
    return user_ratings.dropna()


def anonymise_user_id(user_ratings: pd.DataFrame) -> pd.DataFrame:
    # Anonymise the user_id column by replacing it with a serialised number
    user_mapping = {uid: i for i, uid in enumerate(user_ratings[
        'user_id'
    ].unique(), start=1)}
    user_ratings['user_id'] = user_ratings['user_id'].map(user_mapping)
    return user_ratings


def consolidate_duplicated_movies(user_ratings: pd.DataFrame) -> pd.DataFrame:
    # Consolidate duplicated movies
    # (same movie with different movie_id, where both movie_ids have ratings)
    # into one record
    user_ratings.loc[
        user_ratings["movie_id"] == "ex-machina-2014", "movie_id"
    ] = "ex-machina-2015"
    user_ratings.loc[
        user_ratings["movie_id"] == "black-panther", "movie_id"
    ] = "black-panther-2018"
    return user_ratings


def consolidate_ratings_for_same_movie(
    cleaned_user_ratings: pd.DataFrame
) -> pd.DataFrame:
    # Consolidate ratings for the same movie rated differently by a user
    cleaned_user_ratings = (
        cleaned_user_ratings.groupby(
            ["movie_id", "user_id"],
            as_index=False
        )["rating_val"].mean()
    )
    return cleaned_user_ratings
