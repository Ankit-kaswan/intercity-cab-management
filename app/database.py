from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from app.config import config


Base = declarative_base()

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# print("Creating tables...")
# Base.metadata.create_all(bind=engine, checkfirst=True)
# print("Tables created.")


def get_db():
    """
    Make sure this is singleton
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
