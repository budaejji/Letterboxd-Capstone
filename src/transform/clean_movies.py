import pandas as pd
import ast
from src.utils.file_utils import save_dataframe_to_csv


def clean_movies(movies: pd.DataFrame) -> pd.DataFrame:
    # Task 1 - Remove rows with missing movie_id
    movies = remove_missing_values(movies)
    # Task 2 - Convert genres to list
    movies = convert_genres_to_list(movies)
    # Task 3 - Convert spoken_languages to list
    movies = convert_spoken_languages_to_list(movies)
    # Task 4 - Remove empty strings from spoken_languages
    movies = remove_empty_languages(movies)
    # Task 5 - Standardise runtime format to integer
    movies = standardise_runtime_format(movies)
    # Task 6 - Standardise year_released format to integer
    movies = standardise_year_released_format(movies)
    # Task 7 - Remove any duplicate movie_ids
    movies = movies.drop_duplicates(subset=["movie_id"])
    # Reset index
    movies.reset_index(drop=True, inplace=True)

    # Save the dataframe as a CSV for logging purposes
    # Ensure the directory exists
    output_dir = "data/processed"
    file_name = "cleaned_movies.csv"
    save_dataframe_to_csv(movies, output_dir, file_name)

    return movies


def remove_missing_values(movies: pd.DataFrame) -> pd.DataFrame:
    # Remove rows with missing values in the movie_id column
    movies = movies.dropna(subset=["movie_id"])
    return movies


def convert_genres_to_list(movies: pd.DataFrame) -> pd.DataFrame:
    # Convert the genres column from a string representation of a list to
    # an actual list
    movies['genres'] = movies['genres'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x else []
        )
    return movies


def convert_spoken_languages_to_list(movies: pd.DataFrame) -> pd.DataFrame:
    # Convert the spoken_languages column from a string representation of a
    # list to an actual list
    movies['spoken_languages'] = movies['spoken_languages'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x else [])
    return movies


def remove_empty_languages(movies: pd.DataFrame) -> pd.DataFrame:
    # Remove empty strings from the spoken_languages list
    movies['spoken_languages'] = movies['spoken_languages'].apply(
        lambda x: [language for language in x if language != '']
    )
    return movies


def standardise_runtime_format(movies: pd.DataFrame) -> pd.DataFrame:
    # Convert the runtime column to integer type
    movies['runtime'] = movies['runtime'].astype(int)
    return movies


def standardise_year_released_format(movies: pd.DataFrame) -> pd.DataFrame:
    # Convert the year_released column to integer type
    movies['year_released'] = movies['year_released'].astype(int)
    return movies
