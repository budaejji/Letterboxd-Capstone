import pandas as pd
from unittest.mock import patch
from src.transform.clean_movies_with_ratings import (
    clean_movies_with_ratings,
    drop_id_column,
    convert_date_to_int,
    convert_minute_to_int,
    standardise_ratings
)


def test_drop_id_column():
    df = pd.DataFrame(
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
    result = drop_id_column(df)
    assert "id" not in result.columns
    assert list(result.columns) == ["movie_title", "date", "minute", "rating"]


def test_convert_date_to_int():
    df = pd.DataFrame(
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
    result = convert_date_to_int(df)
    assert result["date"].dtype == pd.Int64Dtype()


def test_convert_minute_to_int():
    df = pd.DataFrame(
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
    result = convert_minute_to_int(df)
    assert result["minute"].dtype == pd.Int64Dtype()


def test_standardise_ratings():
    df = pd.DataFrame(
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

    result = standardise_ratings(df)
    assert result["rating"].iloc[0] == 9.12
    assert result["rating"].iloc[1] == 8.6
    assert result["rating"].iloc[2] == 8.54


class TestCleanMoviesWithRatings:
    @patch("src.transform.clean_movies_with_ratings.save_dataframe_to_csv")
    def test_clean_movies_with_ratings_full_pipeline(self, mock_save):
        df = pd.DataFrame(
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
        
        result = clean_movies_with_ratings(df)

        # Should remove id column
        # Should convert date and minute columns to int type
        # Should double all ratings in rating column

        assert len(result) == 3
        assert "id" not in result.columns
        assert list(result.columns) == ["movie_title", "date", "minute", "rating"]
        assert result["date"].dtype == pd.Int64Dtype()
        assert result["minute"].dtype == pd.Int64Dtype()
        assert result["rating"].iloc[0] == 9.12
        assert result["rating"].iloc[1] == 8.6
        assert result["rating"].iloc[2] == 8.54
        assert mock_save.called

    @patch("src.transform.clean_movies_with_ratings.save_dataframe_to_csv")
    def test_clean_movies_with_ratings_calls_save_function(self, mock_save):
        df = pd.DataFrame(
            {
                "id": [1000002, 1000003, 1000004],
                "movie_title": [
                    "Parasite",
                    "Everything Everywhere All at Once",
                    "Fight Club"
                ],
                "date": [2019, 2022, 1999],
                "minute": [95, 118, 95],
                "rating": [9.02, 8.6, 8.54]
            }
        )

        clean_movies_with_ratings(df)

        mock_save.assert_called_once()
        args, kwargs = mock_save.call_args
        assert args[1] == "data/processed"
        assert args[2] == "cleaned_movies_with_ratings.csv"
