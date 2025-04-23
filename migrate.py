import os
from sqlalchemy import create_engine, Column, Integer, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the base class for ORM models
Base = declarative_base()

# Function to set up the database and create tables
def setup_database(schema=None):
    """
    Set up the database connection and create tables.
    Reads credentials from environment variables.
    :param schema: Optional PostgreSQL schema name (default is 'public').
    """
    # Retrieve PostgreSQL credentials from environment variables
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        raise ValueError("Missing required database credentials in .env file.")

    # Construct the database URL
    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create the database engine
    engine = create_engine(DB_URL, echo=True)  # Set echo=False in production

    # Bind the schema to the metadata if provided
    Base.metadata.schema = schema

    # Create all tables if they don't exist
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
    return engine


# Table: data
class Data(Base):
    __tablename__ = 'data'
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}  # Use schema from .env or default to 'public'

    id = Column(Integer, primary_key=True)
    date = Column(TIMESTAMP, nullable=False)
    real = Column(Float)
    crn = Column(Float)
    cycle_day_number = Column(Float)
    sdn = Column(Float)


# Table: forecast_7
class Forecast7(Base):
    __tablename__ = 'forecast_7'
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}  # Use schema from .env or default to 'public'

    index = Column(Integer, primary_key=True)
    date = Column(TIMESTAMP, nullable=False)
    value = Column(Float)


# Table: forecast_27
class Forecast27(Base):
    __tablename__ = 'forecast_27'
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}  # Use schema from .env or default to 'public'

    index = Column(Integer, primary_key=True)
    date = Column(TIMESTAMP, nullable=False)
    value = Column(Float)


# Table: data_decomposed
class DataDecomposed(Base):
    __tablename__ = 'data_decomposed'
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}  # Use schema from .env or default to 'public'

    id = Column(Integer, primary_key=True)
    date = Column(TIMESTAMP, nullable=False)
    real = Column(Float)
    crn = Column(Float)
    cycle_day_number = Column(Float)
    sdn = Column(Float)
    IMF1 = Column(Float)
    IMF2 = Column(Float)
    IMF3 = Column(Float)
    R = Column(Float)
    IMF1_1 = Column(Float)
    IMF1_2 = Column(Float)
    IMF1_3 = Column(Float)
    IMF2_1 = Column(Float)
    IMF2_2 = Column(Float)
    IMF2_3 = Column(Float)
    IMF3_1 = Column(Float)
    IMF3_2 = Column(Float)
    IMF3_3 = Column(Float)
    R_1 = Column(Float)
    R_2 = Column(Float)
    R_3 = Column(Float)


# Example usage
if __name__ == "__main__":
    try:
        # Set up the database and create tables
        engine = setup_database(schema=os.getenv("DB_SCHEMA", "public"))  # Use schema from .env or default to 'public'

        # Example: Verify tables were created by listing them (optional)
        with engine.connect() as conn:
            result = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema=%s", (os.getenv("DB_SCHEMA", "public"),))
            tables = result.fetchall()
            print("Tables in database:")
            for table in tables:
                print(table[0])
    except Exception as e:
        print(f"An error occurred: {e}")