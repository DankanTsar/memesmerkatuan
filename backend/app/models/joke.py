from .Web3Provider import Merkatuan, send_payable_transaction, onReciept
from .. import db
from ..misc import wait_in_other_thread


Likes = db.Table('Likes', db.Model.metadata,
                 db.Column('User_id', db.Integer, db.ForeignKey('User.user_id')),
                 db.Column('Joke_id', db.Integer, db.ForeignKey('Joke.joke_id')))


class Joke(db.Model):
    __tablename__ = 'Joke'
    joke_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    text = db.Column(db.Text())
    solidity_address = db.Column(db.String(200), nullable=True)
    likes = db.relationship('User', secondary=Likes, backref='likes', lazy='joined')

    def __init__(self, text, user):
        self.text = text
        self.user_id = user.user_id

    def save(self, public=None, private=None):
        if public and private:
            hsh = send_payable_transaction(Merkatuan.functions.addMeme(self.text)
                                     .buildTransaction(dict(gas=3000000)),
                                     public, private)
            def onRecieptCallback(reciept):
                self.solidity_address = Merkatuan.functions.getAllMemes().call()[-1]
                db.session.add(self)
                db.session.commit()
            onReciept(hsh, onRecieptCallback)
        db.session.add(self)
        db.session.commit()

    def remove_joke(self):
        db.session.delete(self)
        db.session.commit()

    def get_text(self):
        return self.text

    def change_text(self, text):
        self.text = text
        self.save()

    def add_like(self, user):
        self.likes.append(user)
        pub, priv = self.likes[-1].get_keys_unsafe()
        send_payable_transaction(Merkatuan.functions.likeMeme(self.solidity_address)
                                 .buildTransaction(dict(gas=3000000)),
                                 pub, priv)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(joke_id=None, get_all=None):
        if joke_id:
            return Joke.query.get(joke_id)

        if get_all:
            jokes = Joke.query
            return jokes
