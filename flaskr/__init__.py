import os
from flask import Flask
from flaskr.database import db_session, init_db

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_URI=os.getenv("DATABASE_URI"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent= True)
    else:
        # Load the test_config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    init_db()

    # a simple page that says Hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    return app
