from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

engine = None
session_maker = sessionmaker(autocommit = False, autoflush=False)
db_session = scoped_session(session_maker)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db(app):
    global engine
    engine = create_engine(app.config['DATABASE_URI'], echo= True)
    session_maker.configure(bind=engine)

    from . import models
    Base.metadata.create_all(bind=engine)