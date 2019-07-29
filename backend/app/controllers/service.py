from .. import app, db

from flask import jsonify
from ..models.joke import Joke
from ..misc.cur_user import cur_user


@app.route('/likeJoke/<int:jid>/', methods=['GET', 'POST'])
def like_joke(jid):
    user = cur_user()
    joke = Joke.get(joke_id=jid)

    if user:
        if user not in joke.likes:
            joke.add_like(user)
        else:
            return "Nop"
    return jsonify([{"likes": str(len(joke.likes))}])
