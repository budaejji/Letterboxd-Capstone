from pathlib import Path
import logging
import os


def _ensure_log_directory(base_path=None):
    """Ensure the logs directory exists."""
    if base_path:
        # Use provided base path (for testing)
        log_directory = Path(base_path) / "logs"
    else:
        # Default to src/logs (current production/dev structure)
        project_root = Path(__file__).resolve().parent.parent
        log_directory = project_root / "logs"  # This resolves to src/logs
    
    log_directory.mkdir(parents=True, exist_ok=True)
    return log_directory


def _create_formatter():
    """Create a standard log formatter."""
    return logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def _create_handlers(log_directory, log_file, level):
    """Create file and console handlers."""
    file_handler = logging.FileHandler(log_directory / log_file)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = _create_formatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    return file_handler, console_handler


def setup_logger(name, log_file, level=logging.DEBUG, base_path=None):
    """Function to setup a logger; can be used in multiple modules."""
    # Check for environment-specific base path
    env_base_path = os.getenv("LOG_BASE_PATH")
    effective_base_path = env_base_path or base_path
    
    log_directory = _ensure_log_directory(effective_base_path)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler, console_handler = _create_handlers(
            log_directory, log_file, level
        )
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def log_extract_success(logger, type, shape, execution_time, expected_rate):
    logger.setLevel(logging.INFO)
    logger.info(f"Data extraction successful for {type}!")
    logger.info(f"Extracted {shape[0]} rows " f"and {shape[1]} columns")
    logger.info(f"Execution time: {execution_time} seconds")

    if execution_time / shape[0] <= expected_rate:
        logger.info(
            "Execution time per row: " f"{execution_time / shape[0]} seconds"
        )
    else:
        logger.setLevel(logging.WARNING)
        logger.warning(
            f"Execution time per row exceeds {expected_rate}: "
            f"{execution_time / shape[0]} seconds"
        )
