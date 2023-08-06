from flask import Response


def add_cors_headers(response: Response) -> Response:
    res = response
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
