import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY")

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn
