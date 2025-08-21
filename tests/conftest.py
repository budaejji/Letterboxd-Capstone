import pytest
import os
from config.env_config import setup_env


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Automatically set up the test environment for all tests.
    This fixture runs once per test session and ensures that
    the test environment variables are loaded before any tests run.
    """
    # Only set up test environment if ENV is not already set or is set to 'test'
    current_env = os.environ.get('ENV')
    if current_env is None or current_env == 'test':
        setup_env(["pytest", "test"])
    
    yield
    
    # Cleanup is handled by the setup_env function's cleanup_previous_env