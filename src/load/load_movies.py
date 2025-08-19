import pandas as pd
from src.load.load_df_to_db import load_dataframe_to_db


def load_movies(movies_df: pd.DataFrame) -> pd.DataFrame:
    load_dataframe_to_db(movies_df, table_name="rf_movies")
    return movies_df
