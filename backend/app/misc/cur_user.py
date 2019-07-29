from flask import session
from ..models.User import User


def cur_user():
    if 'Username' in session:
        return User.get(username=session['Username'])
    return None
