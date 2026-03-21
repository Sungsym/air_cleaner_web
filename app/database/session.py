from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.config import settings

# db_url = "sqlite:///database.db"
db_url = settings.POSTGRES_URL
engine = create_engine(db_url, echo=True)

def create_db_and_tables():
    from app.database.models import Air
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

