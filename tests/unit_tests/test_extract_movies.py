import pandas as pd
import pytest
import re
from src.extract.extract_movies import (
    extract_movies,
    TYPE,
    FILE_PATH,
    EXPECTED_PERFORMANCE,
)


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch("src.extract.extract_movies.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.extract.extract_movies.logger")


def test_extract_movies_csv_to_dataframe(mocker):
    mock_df = pd.DataFrame(
        {
            "movie_id": ["napoleon-dynamite", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                "[""Comedy""]",
                "[""Crime"",""Mystery"",""Thriller""]",
                "[""Adventure"",""Animation"",""Comedy"",""Family""]"
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                "[""English""]",
                "[""English""]",
                "[""English""]"
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )

    mocker.patch(
        "src.extract.extract_movies.pd.read_csv", return_value=mock_df
    )

    # Call the function
    df = extract_movies()

    # Assertions
    assert isinstance(df, pd.DataFrame)
    pd.testing.assert_frame_equal(df, mock_df)


def test_log_extract_success_movies(
    mocker, mock_log_extract_success, mock_logger
):
    mock_execution_time = 0.5
    mock_df = pd.DataFrame(
        {
            "movie_id": ["napoleon-dynamite", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                "[""Comedy""]",
                "[""Crime"",""Mystery"",""Thriller""]",
                "[""Adventure"",""Animation"",""Comedy"",""Family""]"
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                "[""English""]",
                "[""English""]",
                "[""English""]"
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )

    mocker.patch(
        "src.extract.extract_movies.pd.read_csv", return_value=mock_df
    )

    # Mock timeit.default_timer to control the execution time
    mock_start_time = 100.0
    mock_end_time = 100.5
    mocker.patch(
        "src.extract.extract_movies.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time],
    )

    # Call the function
    df = extract_movies()

    # Assertions
    mock_log_extract_success.assert_called_once_with(
        mock_logger, TYPE, df.shape, mock_execution_time, EXPECTED_PERFORMANCE
    )


def test_log_movies_error(mocker, mock_logger):
    # Mock pd.read_csv to raise an exception
    mocker.patch(
        "src.extract.extract_movies.pd.read_csv",
        side_effect=Exception(f"Failed to load CSV file: {FILE_PATH}"),
    )

    # Call the function and assert exception
    with pytest.raises(
        Exception, match=re.escape(f"Failed to load CSV file: {FILE_PATH}")
    ):
        extract_movies()

    # Verify that the error was logged
    mock_logger.error.assert_called_once_with(
        f"Error loading {FILE_PATH}: Failed to load CSV file: {FILE_PATH}"
    )
