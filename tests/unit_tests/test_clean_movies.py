import pandas as pd
from unittest.mock import patch
from src.transform.clean_movies import (
    clean_movies,
    remove_missing_values,
    convert_genres_to_list,
    convert_spoken_languages_to_list,
    remove_empty_languages,
    standardise_runtime_format,
    standardise_year_released_format
)


def test_remove_missing_values():
    df = pd.DataFrame(
        {
            "movie_id": ["", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                '["Comedy"]',
                '["Crime","Mystery","Thriller"]',
                '["Adventure","Animation","Comedy","Family"]'
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                '["English"]',
                '["English"]',
                '["English"]'
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )
    result = remove_missing_values(df)
    assert len(result) == 2
    assert result["movie_id"].tolist() == ["insomnia-2002", "a-bugs-life"]


def test_convert_genres_to_list():
    df = pd.DataFrame(
        {
            "movie_id": ["", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                '["Comedy"]',
                '["Crime","Mystery","Thriller"]',
                '["Adventure","Animation","Comedy","Family"]'
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                '["English"]',
                '["English"]',
                '["English"]'
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )
    result = convert_genres_to_list(df)
    assert isinstance(result["genres"].iloc[0], list)
    assert result["genres"].tolist() == [
        ["Comedy"],
        ["Crime", "Mystery", "Thriller"],
        ["Adventure", "Animation", "Comedy", "Family"]
    ]


def test_convert_spoken_languages_to_list():
    df = pd.DataFrame(
        {
            "movie_id": ["", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                '["Comedy"]',
                '["Crime","Mystery","Thriller"]',
                '["Adventure","Animation","Comedy","Family"]'
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                '["English"]',
                '["English"]',
                '["English"]'
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )
    result = convert_spoken_languages_to_list(df)
    assert isinstance(result["spoken_languages"].iloc[0], list)
    assert result["spoken_languages"].tolist() == [
        ["English"],
        ["English"],
        ["English"]
    ]


def test_remove_empty_languages():
    df = pd.DataFrame(
        {
            "movie_id": ["", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                '[""Comedy""]',
                '[""Crime"",""Mystery"",""Thriller""]',
                '[""Adventure"",""Animation"",""Comedy"",""Family""]'
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                ["English", ""],
                [""],
                ["English"]
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )
    result = remove_empty_languages(df)
    assert result["spoken_languages"].iloc[0] == ["English"]
    assert result["spoken_languages"].iloc[1] == []


def test_standardise_runtime_format():
    df = pd.DataFrame(
        {
            "movie_id": ["", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                '["Comedy"]',
                '["Crime","Mystery","Thriller"]',
                '["Adventure","Animation","Comedy","Family"]'
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                    '["English"]',
                    '["English"]',
                    '["English"]'
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )
    result = standardise_runtime_format(df)
    assert result["runtime"].iloc[0] == 95
    assert result["runtime"].dtype == "int64"


def test_standardise_year_released_format():
    df = pd.DataFrame(
        {
            "movie_id": ["", "insomnia-2002", "a-bugs-life"],
            "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
            "genres": [
                '["Comedy"]',
                '["Crime","Mystery","Thriller"]',
                '["Adventure","Animation","Comedy","Family"]'
            ],
            "original_language": ["en", "en", "en"],
            "image_url": [
                "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
            ],
            "runtime": [95.0, 118.0, 95.0],
            "spoken_languages": [
                '["English"]',
                '["English"]',
                '["English"]'
            ],
            "year_released": [2004.0, 2002.0, 1998.0]
        }
    )
    result = standardise_year_released_format(df)
    assert result["year_released"].iloc[0] == 2004
    assert result["year_released"].dtype == "int64"


class TestCleanMovies:
    @patch("src.transform.clean_movies.save_dataframe_to_csv")
    def test_clean_movies_full_pipeline(self, mock_save):
        df = pd.DataFrame(
            {
                "movie_id": ["", "insomnia-2002", "a-bugs-life"],
                "movie_title": ["Napoleon Dynamite", "Insomnia", "A Bug's Life"],
                "genres": [
                    '["Comedy"]',
                    '["Crime","Mystery","Thriller"]',
                    '["Adventure","Animation","Comedy","Family  "]'
                ],
                "original_language": ["en", "en", "en"],
                "image_url": [
                    "sm/upload/wu/r9/ma/tt/2VMXuUAvU8T0oQl0w77CqVARxYs-0-230-0-345-crop",
                    "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                    "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
                ],
                "runtime": [95.0, 118.0, 95.0],
                "spoken_languages": [
                    '["English"]',
                    '["English"]',
                    '["English"]'
                ],
                "year_released": [2004.0, 2002.0, 1998.0]
            }
        )
        result = clean_movies(df)

        # Should remove row with missing movie_id (first record)
        # Should convert genres and spoken_languages to list
        # Should remove empty strings from spoken_languages
        # Should standardise runtime and year_released formats

        assert len(result) == 2
        assert result["genres"].dtype == list
        assert result["spoken_languages"].dtype == list
        assert result["runtime"].iloc[0] == 118
        assert result["runtime"].dtype == int
        assert result["year_released"].iloc[0] == 2002
        assert result["year_released"].dtype == int
        assert mock_save.called

    @patch("src.transform.clean_movies.save_dataframe_to_csv")
    def test_clean_movies_calls_save_function(self, mock_save):
        df = pd.DataFrame(
            {
                "movie_id": ["insomnia-2002", "a-bugs-life"],
                "movie_title": ["Insomnia", "A Bug's Life"],
                "genres": [
                    ["Crime", "Mystery", "Thriller"],
                    ["Adventure", "Animation", "Comedy", "Family"]
                ],
                "original_language": ["en", "en"],
                "image_url": [
                    "film-poster/5/1/7/3/9/51739-insomnia-0-230-0-345-crop",
                    "film-poster/4/7/1/1/1/47111-a-bug-s-life-0-230-0-345-crop"
                ],
                "runtime": [118, 95],
                "spoken_languages": [
                    [],
                    ["English"]
                ],
                "year_released": [2002, 1998]
            }
        )

        clean_movies(df)

        mock_save.assert_called_once()
        args, kwargs = mock_save.call_args
        assert args[1] == "data/processed"
        assert args[2] == "cleaned_movies.csv"
