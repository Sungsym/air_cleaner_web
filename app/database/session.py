from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session


db = "sqlite:///database.db"
engine = create_engine(db, echo=True)

def create_db_and_tables():
    from app.database.models import Air
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
