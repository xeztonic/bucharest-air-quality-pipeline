import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def get_connection():
    """Open a connection to PostgreSQL using the settings from .env."""
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )