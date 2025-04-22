from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base
from migrate import Data
from db.CRUD import CRUD


class DataTable:
    def __init__(
        self,
        **kwargs
    ):

        Base = declarative_base()
        # Load environment variables from .env file
        load_dotenv()

        # Create a database engine
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME")

        if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
            raise ValueError("Missing required database credentials in .env file.")

        DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DB_URL, echo=True)

        # Create a session factory
        SessionLocal = sessionmaker(bind=engine)

        # Instantiate the DataCRUD class
        model = CRUD(Data)