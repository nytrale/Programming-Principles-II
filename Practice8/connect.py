import psycopg2
from config import DB_config

def get_connection():
    return psycopg2.connect(**DB_config)