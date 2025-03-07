from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("DATABASE_URI"))
engine = create_engine(os.getenv("DATABASE_URI"), echo= True)
db_session = scoped_session(sessionmaker(autocommit = False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)