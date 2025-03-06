from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from database import db_session, init_db

app = Flask(__name__)
# TO DO introduce config
# app.config.from_object(Config)

# db=SQLAlchemy(app)
# migrate=Migrate(app,db)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

init_db()

from models import TaskStatusTypes

status_not_started = TaskStatusTypes('Not Started', 'This status means that the tasks planned start date hasn\'t begin yet.')
db_session.add(status_not_started)
db_session.commit()
TaskStatusTypes.query.all()
TaskStatusTypes.query.filter(TaskStatusTypes.status == 'Not Started').first()

