import pandas as pd
from unittest.mock import patch
from src.transform.clean_user_ratings import (
    clean_user_ratings,
    remove_missing_values,
    anonymise_user_id,
    consolidate_duplicated_movies,
    consolidate_ratings_for_same_movie
)


def test_remove_missing_values():
    df = pd.DataFrame(
        {
            "movie_id": ["mank", "the-social-network", "insidious"],
            "rating_val": [5, None, 10],
            "user_id": ["deathproof", "lily", "bob"]
        }
    )
    result = remove_missing_values(df)
    assert result.shape[0] == 2


def test_anonymise_user_id():
    df = pd.DataFrame(
        {
            "movie_id": ["mank", "the-social-network", "insidious"],
            "rating_val": [5, 8, 10],
            "user_id": ["deathproof", "lily", "bob"]
        }
    )
    result = anonymise_user_id(df)
    assert result["user_id"].iloc[0] == 1
    assert result["user_id"].iloc[1] == 2
    assert result["user_id"].iloc[2] == 3


def test_consolidate_duplicated_movies():
    df = pd.DataFrame(
        {
            "movie_id": ["ex-machina-2014", "ex-machina-2015", "insidious"],
            "rating_val": [5, 8, 10],
            "user_id": ["deathproof", "lily", "bob"]
        }
    )
    result = consolidate_duplicated_movies(df)
    assert result["movie_id"].iloc[0] == "ex-machina-2015"
    assert result["movie_id"].iloc[1] == "ex-machina-2015"
    assert result["movie_id"].iloc[2] == "insidious"


def test_consolidate_ratings_for_same_movie():
    df = pd.DataFrame(
        {
            "movie_id": ["ex-machina-2015", "ex-machina-2015", "insidious"],
            "rating_val": [6, 8, 10],
            "user_id": ["deathproof", "deathproof", "bob"]
        }
    )

    result = consolidate_ratings_for_same_movie(df)
    assert result["rating_val"].iloc[0] == 7
    assert result.shape[0] == 2


class TestCleanUserRatings:
    @patch("src.transform.clean_user_ratings.save_dataframe_to_csv")
    def test_clean_user_ratings_full_pipeline(self, mock_save):
        df = pd.DataFrame(
            {
                "movie_id": ["ex-machina-2015", "ex-machina-2014", "insidious", "mank"],
                "rating_val": [6, 8, 10, None],
                "user_id": ["deathproof", "deathproof", "bob", "lily"]
            }
        )
        
        result = clean_user_ratings(df)

        # Should remove rows with missing values
        # Should anonymise user id
        # Should consolidate duplicated movies
        # Should consolidate duplicated ratings

        assert len(result) == 2
        assert result["user_id"].iloc[0] == 1
        assert result["user_id"].iloc[1] == 2
        assert result["movie_id"].iloc[0] == "ex-machina-2015"
        assert result["movie_id"].iloc[1] == "insidious"
        assert result["rating_val"].iloc[0] == 7
        assert mock_save.called

    @patch("src.transform.clean_user_ratings.save_dataframe_to_csv")
    def test_clean_user_ratings_calls_save_function(self, mock_save):
        df = pd.DataFrame(
            {
                "movie_id": ["ex-machina-2015", "ex-machina-2015", "insidious"],
                "rating_val": [6, 8, 10],
                "user_id": ["deathproof", "deathproof", "bob"]
            }
        )

        clean_user_ratings(df)

        mock_save.assert_called_once()
        args, kwargs = mock_save.call_args
        assert args[1] == "data/processed"
        assert args[2] == "cleaned_user_ratings.csv"
