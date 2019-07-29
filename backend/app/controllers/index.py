from .. import app
from flask import render_template
from ..misc.cur_user import cur_user


@app.route("/")
def index():
    return render_template("index.html", user=cur_user())
