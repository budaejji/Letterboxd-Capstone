import pandas as pd
from src.load.load_df_to_db import load_dataframe_to_db


def load_aggregated_user_ratings(
    aggregated_user_ratings_df: pd.DataFrame
) -> pd.DataFrame:
    load_dataframe_to_db(
        aggregated_user_ratings_df,
        table_name="rf_aggregated_user_ratings"
    )
    return aggregated_user_ratings_df
