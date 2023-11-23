# config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_env_variable(key, default_value=None):
    value = os.getenv(key, default_value)
    if value is None:
        raise ValueError(f"Environment variable {key} not found.")
    return value
