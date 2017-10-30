from flask import Flask
from utils import json_response


app = Flask(__name__)


@app.errorhandler(404)
def error_404(err):
    return json_response(err=True, message='Not found')

from library_app import endpoint
