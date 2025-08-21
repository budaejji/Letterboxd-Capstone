import pandas as pd
import pytest
import re
from src.extract.extract_movies_with_ratings import (
    extract_movies_with_ratings,
    TYPE,
    FILE_PATH,
    EXPECTED_PERFORMANCE,
)


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch(
        "src.extract.extract_movies_with_ratings.log_extract_success"
    )


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.extract.extract_movies_with_ratings.logger")


def test_extract_movies_with_ratings_csv_to_dataframe(mocker):
    mock_df = pd.DataFrame(
        {
            "id": [1000002, 1000003, 1000004],
            "movie_title": [
                "Parasite",
                "Everything Everywhere All at Once",
                "Fight Club"
            ],
            "date": [2019.0, 2022.0, 1999.0],
            "minute": [95.0, 118.0, 95.0],
            "rating": [4.56, 4.3, 4.27]
        }
    )

    mocker.patch(
        "src.extract.extract_movies_with_ratings.pd.read_csv",
        return_value=mock_df
    )

    # Call the function
    df = extract_movies_with_ratings()

    # Assertions
    assert isinstance(df, pd.DataFrame)
    pd.testing.assert_frame_equal(df, mock_df)


def test_log_extract_success_movies_with_ratings(
    mocker, mock_log_extract_success, mock_logger
):
    mock_execution_time = 0.5
    mock_df = pd.DataFrame(
        {
            "id": [1000002, 1000003, 1000004],
            "movie_title": [
                "Parasite",
                "Everything Everywhere All at Once",
                "Fight Club"
            ],
            "date": [2019.0, 2022.0, 1999.0],
            "minute": [95.0, 118.0, 95.0],
            "rating": [4.56, 4.3, 4.27]
        }
    )

    mocker.patch(
        "src.extract.extract_movies_with_ratings.pd.read_csv",
        return_value=mock_df
    )

    # Mock timeit.default_timer to control the execution time
    mock_start_time = 100.0
    mock_end_time = 100.5
    mocker.patch(
        "src.extract.extract_movies_with_ratings.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time],
    )

    # Call the function
    df = extract_movies_with_ratings()

    # Assertions
    mock_log_extract_success.assert_called_once_with(
        mock_logger, TYPE, df.shape, mock_execution_time, EXPECTED_PERFORMANCE
    )


def test_log_movies_with_ratings_error(mocker, mock_logger):
    # Mock pd.read_csv to raise an exception
    mocker.patch(
        "src.extract.extract_movies_with_ratings.pd.read_csv",
        side_effect=Exception(f"Failed to load CSV file: {FILE_PATH}"),
    )

    # Call the function and assert exception
    with pytest.raises(
        Exception, match=re.escape(f"Failed to load CSV file: {FILE_PATH}")
    ):
        extract_movies_with_ratings()

    # Verify that the error was logged
    mock_logger.error.assert_called_once_with(
        f"Error loading {FILE_PATH}: Failed to load CSV file: {FILE_PATH}"
    )
