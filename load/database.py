import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
class Database:
    
    def __init__(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DB")
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")

        self.url = (
            f"postgresql+psycopg2://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/"
            f"{self.database}"
        )

        self.engine = create_engine(self.url)
        
