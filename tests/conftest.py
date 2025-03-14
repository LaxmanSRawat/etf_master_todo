import pytest
from flaskr import create_app
from flaskr.database import Base, db_session, engine, init_db
from sqlalchemy import text
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
    
    db_engine = init_db(app,engine)
    Base.metadata.create_all(bind=db_engine)

    session = db_session()
    session.execute(text("PRAGMA foreign_keys = 1;"))
    yield session

    session.rollback()
    session.close()
    db_session.remove()
    Base.metadata.drop_all(bind = db_engine)

@pytest.fixture(scope = "module")
def client(app):
    return app.test_client()
