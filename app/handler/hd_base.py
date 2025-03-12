from flask import request, make_response
import functools
from app import app

import flask

# 请求参数校验
def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in required_args:
                if arg not in request.json:
                    return flask.abort(400)
            return func(*args, **kw) 
        return wrapper
    return decorator

@app.errorhandler(400)
def not_found(error): 
     return make_response(flask.jsonify({'error': '必传参数未传入，参数不正确'}), 400)