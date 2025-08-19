from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, OperationalError, SQLAlchemyError
import logging
from src.utils.logging_utils import setup_logger


class DatabaseConnectionError(Exception):
    pass


class QueryExecutionError(Exception):
    pass


# Configure the logger
logger = setup_logger(__name__, "database.log", level=logging.DEBUG)


def create_db_engine(connection_params):
    try:
        for param in ["dbname", "user", "password", "host", "port"]:
            if not param == "password" and not connection_params.get(param):
                raise ValueError(f"{param} not provided")
        engine = create_engine(
            f"postgresql+psycopg://{connection_params['user']}"
            f":{connection_params['password']}@{connection_params['host']}"
            f":{connection_params['port']}/{connection_params['dbname']}"
        )
        logger.setLevel(logging.INFO)
        logger.info("Successfully created the database engine.")
        return engine
    except ArgumentError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Invalid Connection Parameters: {e}")
        raise DatabaseConnectionError(f"Invalid Connection Parameters: {e}")
    except ImportError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Invalid DB Driver: {e}")
        raise DatabaseConnectionError(f"Invalid DB Driver: {e}")
    except ValueError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Invalid Connection Parameters: {e}")
        raise DatabaseConnectionError(f"Invalid Connection Parameters: {e}")


def get_db_connection(connection_params):
    try:
        engine = create_db_engine(connection_params)
        connection = engine.connect()
        logger.setLevel(logging.INFO)
        logger.info("Successfully connected to the database.")
        return connection
    except OperationalError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Operational error when connecting to the database: {e}")
        raise DatabaseConnectionError(
            f"Operational error when connecting to the database: {e}"
        )
    except SQLAlchemyError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Failed to connect to the database: {e}")
        raise DatabaseConnectionError(
            f"Failed to connect to the database: {e}"
        )
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
