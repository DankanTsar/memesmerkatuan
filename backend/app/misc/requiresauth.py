from functools import wraps
from .cur_user import cur_user
from flask import redirect, url_for


def requiresauth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if cur_user() is None:
            return redirect(url_for('log'))
        return f(*args, **kwargs)

    return wrapped
