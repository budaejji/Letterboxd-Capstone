import pandas as pd
from src.utils.file_utils import save_dataframe_to_csv


def enrich_movies_table_with_user_ratings_data(
    merged_data: pd.DataFrame, cleaned_user_ratings: pd.DataFrame
) -> pd.DataFrame:
    """
    Creates new table with aggregated average rating and rating count for
    each user.

    Args:
        merged_data (pd.DataFrame): The DataFrame containing movies merged with
        the average rating on Letterboxd.
        cleaned_user_ratings (pd.DataFrame): The DataFrame containing cleaned
        user ratings data.

    Returns:
        pd.DataFrame: A DataFrame containing each movie enriched with the
        average rating and rating count from the user ratings data.
    """
    merged_enriched = merged_data.merge(
        aggregate_average_rating_of_each_movie_by_users(cleaned_user_ratings),
        on="movie_id", how="left"
    )
    # Merge rating count to movies table
    merged_enriched = merged_enriched.merge(
        aggregate_user_count_for_each_movie(cleaned_user_ratings),
        on="movie_id", how="left"
    )
    # Reset index
    merged_enriched.reset_index(drop=True, inplace=True)
    # Save the merged data to a CSV file
    output_dir = "data/processed/"
    file_name = "merged_enriched_movies.csv"
    save_dataframe_to_csv(merged_enriched, output_dir, file_name)

    return merged_enriched


def aggregate_average_rating_of_each_movie_by_users(
    cleaned_user_ratings: pd.DataFrame
) -> pd.DataFrame:
    # Find average rating for each movie as rated by our userbase
    avg_ratings = (
        cleaned_user_ratings.groupby("movie_id")["rating_val"]
        .mean()
        .reset_index()
    )
    avg_ratings.rename(
        columns={"rating_val": "power_users_rating"},
        inplace=True
    )
    # Round the average ratings to two decimal places
    avg_ratings["power_users_rating"] = (
        avg_ratings["power_users_rating"].round(2)
    )

    return avg_ratings


def aggregate_user_count_for_each_movie(
    cleaned_user_ratings: pd.DataFrame
) -> pd.DataFrame:
    # Count the number of users who rated each movie
    ratings_count = (
        cleaned_user_ratings.groupby("movie_id")["rating_val"]
        .count()
        .reset_index()
    )
    ratings_count.rename(columns={"rating_val": "ratings_count"}, inplace=True)
    return ratings_count
