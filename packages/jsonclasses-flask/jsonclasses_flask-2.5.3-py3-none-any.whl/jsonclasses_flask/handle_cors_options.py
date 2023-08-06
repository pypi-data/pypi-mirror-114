from typing import Optional
from flask import request, Response, current_app


def handle_cors_options() -> Optional[Response]:
    if request.method == 'OPTIONS':
        res = current_app.response_class()
        res.status_code = 204
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST, GET, PATCH, DELETE'
        res.headers['Access-Control-Allow-Headers'] = '*'
        res.headers['Access-Control-Max-Age'] = '86400'
        return res
    return None
