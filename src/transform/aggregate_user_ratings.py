import pandas as pd
from src.utils.file_utils import save_dataframe_to_csv


def aggregate_user_ratings(cleaned_user_ratings: pd.DataFrame) -> pd.DataFrame:
    """
    Creates new table with aggregated average rating and rating count for
    each user.

    Args:
        cleaned_user_ratings (pd.DataFrame): The DataFrame containing cleaned
        user ratings data.

    Returns:
        pd.DataFrame: A DataFrame containing average rating and rating count
        for each user.
    """
    aggregated_user_ratings = find_user_average_rating(
        cleaned_user_ratings
    ).merge(
        find_user_rating_count(cleaned_user_ratings), on="user_id", how="left"
    )
    # Reset index
    aggregated_user_ratings.reset_index(drop=True, inplace=True)
    # Save the new table to a CSV file
    output_dir = "data/processed/"
    file_name = "aggregated_user_ratings.csv"
    save_dataframe_to_csv(aggregated_user_ratings, output_dir, file_name)
    return aggregated_user_ratings


def find_user_average_rating(
    cleaned_user_ratings: pd.DataFrame
) -> pd.DataFrame:
    # Find the average rating given by a specific user
    user_average_rating = cleaned_user_ratings.groupby(
        "user_id"
    )["rating_val"].mean().reset_index()
    # Rename the column for clarity
    user_average_rating.rename(columns={"rating_val": "user_average_rating"},
                               inplace=True)
    # Round the average rating to two decimal places
    user_average_rating["user_average_rating"] = user_average_rating[
        "user_average_rating"
    ].round(2)
    return user_average_rating


def find_user_rating_count(cleaned_user_ratings: pd.DataFrame) -> pd.DataFrame:
    # Find the number of ratings given by a specific user
    user_rating_count = cleaned_user_ratings.groupby("user_id").size(
        ).reset_index(
        name="rating_count"
    )
    return user_rating_count
