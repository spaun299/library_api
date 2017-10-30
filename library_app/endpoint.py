from flask import abort, request
from utils import json_response
from . import app


@app.route('/api/books', methods=["GET", ])
def list_books():
    return json_response(books=[])


@app.route('/api/books/<string:title>', methods=["GET", ])
def get_book(title):
    return json_response(book={'title': title})


@app.route('/api/books', methods=["POST", ])
def create_book():
    body = request.form
    return json_response(created=True, id=123)


@app.route('/api/books/<string:title>', methods=["PUT", ])
def update_book(title):
    price = request.form.get('price')
    return json_response(updated=True)
