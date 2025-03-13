import pytest
from flaskr import create_app
from flaskr.database import Base, db_session, engine, init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import flaskr.models
from flaskr.database import Base

@pytest.fixture(scope="module")
def app():
    test_config = {
        "DATABASE_URI" : "sqlite:///:memory:",
        "TESTING": True
    }
    app = create_app(test_config)

    yield app

@pytest.fixture(scope="module")
def session(app):
    # engine = create_engine(app.config["DATABASE_URI"])
    # db_session = scoped_session(sessionmaker(bind=engine))
    # session = db_session()
    # Base.query = db_session.query_property()
    # Base.metadata.create_all(bind=engine)
    
    db_engine = init_db(app,engine)
    Base.metadata.create_all(bind=db_engine)

    session = db_session()
    yield session

    session.rollback()
    session.close()
    db_session.remove()
    Base.metadata.drop_all(bind = db_engine)

@pytest.fixture(scope = "module")
def client(app):
    return app.test_client()
