from flask import render_template
from .. import app
from ..misc.cur_user import cur_user


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html', user=cur_user()), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', user=cur_user()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', user=cur_user()), 500
