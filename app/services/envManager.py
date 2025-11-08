import os

from dotenv import load_dotenv


def get_env_variable(key):
    # Load environment variables from .env file
    load_dotenv()

    # Get the value of the specified key
    value = os.getenv(key)

    if value is None:
        raise KeyError(f"Key '{key}' not found in the environment variables.")

    return value
