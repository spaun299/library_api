from flask import jsonify


def json_response(err=False, **kwargs):
    kwargs.update(dict(err=True if err else False))
    return jsonify(kwargs)
