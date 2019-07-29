from .. import app

from flask import render_template
from ..forms.joke import JokeForm
from ..models.joke import Joke
from ..misc.cur_user import cur_user
from ..misc.requiresauth import requiresauth


@app.route("/add_joke", methods=['GET', 'POST'])
@requiresauth
def add_joke():
    form = JokeForm()

    user = cur_user()

    if form.validate_on_submit():
        joke = Joke(form.joke_text.data, user)  # TODO replace "1" with user id when it is implemented
        pub, priv = user.get_keys(form.joke_password.data)
        joke.save(pub, priv)

    pack = Joke.get(get_all=True)

    return render_template("joke.html", form=form, items=pack)
