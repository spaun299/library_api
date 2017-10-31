from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import json_response, get_database_uri
import config


app = Flask(__name__)
app.config.from_object(config)
config_fields = ('DB_HOST', 'DB_USERNAME', 'DB_PASSWORD', 'DB_NAME')
for field in config_fields:
    if not app.config.get(field, None):
        raise ValueError("Please specify '%s' in config file" % field)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=get_database_uri(
        app.config.get('DB_HOST'), app.config.get('DB_USERNAME'),
        app.config.get('DB_PASSWORD'), app.config.get('DB_NAME'))))


@app.errorhandler(404)
def error_404(err):
    return json_response(err=True, message='Not found', code=404)


@app.errorhandler(400)
def error_404(err):
    return json_response(err=True, message='Bad request', code=400)


def load_db_session(db_url):
    engine = create_engine(db_url,
                           echo=False)
    sql_connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    g.db = db_session
    g.db_connection = sql_connection
    g.engine = engine


from library_app import endpoint
