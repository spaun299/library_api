from flask import jsonify
import datetime
import logging


def json_response(err=False, **kwargs):
    kwargs.update(dict(err=True if err else False))
    if err and kwargs.get('message'):
        logging.debug(kwargs['message'])
    return jsonify(kwargs)


def get_database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name,
                  'host': host,
                  'username': username,
                  'password': password})


def timestamp_to_date(ts: int):
    return datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
