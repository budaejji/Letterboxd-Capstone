import pandas as pd
from src.load.load_df_to_db import load_dataframe_to_db


def load_user_ratings(user_ratings_df: pd.DataFrame) -> pd.DataFrame:
    load_dataframe_to_db(user_ratings_df, table_name="rf_user_ratings")
    return user_ratings_df
