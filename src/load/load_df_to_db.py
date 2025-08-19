import logging
import pandas as pd
from config.db_config import load_db_config
from src.utils.db_utils import get_db_connection

logger = logging.getLogger(__name__)


def load_dataframe_to_db(
    df: pd.DataFrame,
    table_name: str,
):
    try:
        connection_details = load_db_config()["target_database"]
        print(connection_details)
        connection = get_db_connection(connection_details)
        logger.info(f"Loading DataFrame to table '{table_name}' in database.")
        df.to_sql(
            table_name,
            connection,
            schema="de_2506_a",
            index=False,
            if_exists="replace"
        )
        connection.close()
        logger.info(
            f"Successfully loaded table '{table_name}' with {len(df)} records."
        )
    except Exception as e:
        logger.error(f"Failed to load table '{table_name}': {e}")
        raise
