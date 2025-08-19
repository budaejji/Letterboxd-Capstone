import pandas as pd


def merge_movies_and_movies_with_ratings(
    cleaned_movies: pd.DataFrame, cleaned_movies_with_ratings: pd.DataFrame
) -> pd.DataFrame:
    # Merge movies with movies_with_ratings on movie title and year released
    merged_data = cleaned_movies.merge(
        cleaned_movies_with_ratings[['name', 'date', 'rating']],
        left_on=['movie_title', 'year_released'],
        right_on=['name', 'date'],
        how='left'
    )
    # Drop the extra columns from movies_with_ratings
    merged_data = merged_data.drop(columns=['name', 'date'])
    # Some duplicates introduced due to joining method
    # Drop duplicated movie records without rating and keep only the movie
    # with rating data
    merged_data = merged_data.sort_values(by='rating', ascending=False)
    # Drop duplicates based on movie_id, keeping the first occurrence
    # (the one with a rating)
    merged_data = merged_data.drop_duplicates(
        subset=['movie_id'], keep='first'
    )
    # Remove same movies with different movie_id
    # ("Ex Machina" and "Black Panther")
    merged_data = merged_data[merged_data["movie_id"] != "ex-machina-2014"]
    merged_data = merged_data[merged_data["movie_id"] != "black-panther"]
    # Drop records without rating data
    merged_data = merged_data.dropna(subset=['rating'])
    # Reset index
    merged_data.reset_index(drop=True, inplace=True)
    # Merged data ready to be enriched by user ratings data

    return merged_data
