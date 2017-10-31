from flask import request, g, abort
from utils import json_response, timestamp_to_date
from .models import Book, Author
from . import app, auth


@app.route('/api/books', methods=["GET", ])
def list_books():
    books = []
    for b in g.db.query(Book).all():
        books.append(b.book_to_dict())
    return json_response(books=books)


@app.route('/api/books/<string:title>', methods=["GET", ])
def get_book(title):
    if not isinstance(title, str):
        return json_response(err=True,
                             message="title should be string, got %s" % type(
                                 title),
                             code=400)
    book = g.db.query(Book).filter_by(name=title).first()
    if not book:
        abort(404)
    return json_response(book=book.book_to_dict())


@app.route('/api/books', methods=["POST", ])
@auth.login_required
def create_book():
    body = request.json
    required_fields = {'name': str, 'author': str, 'published': int, 'price': float}
    for field, t in required_fields.items():
        body_field = body.get(field, None)
        if not body_field:
            return json_response(err=True,
                                 message="Please provide field '%s' in the request body" %
                                         field,
                                 code=400)
        elif not isinstance(body_field, t):
            return json_response(err=True,
                                 message="Type of field '%s' should be '%s', got '%s'" % (
                                     field, t, type(body_field)),
                                 code=400)
    book = Book.query_by_name(body.get('name'))
    if book:
        return json_response(err=True,
                             message="Book already exists",
                             code=400)
    author = Author.query_by_name(body['author'])
    book_id = Book(name=body['name'], publish_date=timestamp_to_date(body['published']),
                   price=body['price'], author=author or Author(name=body['author'])).save()
    return json_response(id=book_id)


@app.route('/api/books/<string:title>', methods=["PUT", ])
@auth.login_required
def update_book(title):
    price = request.json.get('price')
    if not isinstance(title, str):
        return json_response(err=True,
                             message="title should be string, got %s" % type(
                                 title),
                             code=400)
    elif not (isinstance(price, float) or isinstance(price, int)):
        return json_response(err=True,
                             message="price should be float or int, got %s" % type(
                                 price),
                             code=400)
    book = Book.query_by_name(title)
    if not book:
        abort(404)
    book_id = book.update_price(price)
    return json_response(id=book_id)


@app.route('/api/books/<string:title>', methods=["DELETE", ])
@auth.login_required
def delete_book(title):
    if not isinstance(title, str):
        return json_response(err=True,
                             message="title should be string, got %s" % type(
                                 title),
                             code=400)
    book = Book.query_by_name(title)
    if not book:
        abort(404)
    book_id = book.delete()
    return json_response(id=book_id)
