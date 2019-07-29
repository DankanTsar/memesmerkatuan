from .. import db, bcrypt
import secrets
from Crypto.Cipher import CAST



class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String(60), nullable=False)
    pubkey = db.Column(db.String(254), nullable=False)
    privkey = db.Column(db.String(254), nullable=False)

    pubkey_1 = db.Column(db.String(254), nullable=False)
    privkey_1 = db.Column(db.String(254), nullable=False)

    jokes = db.relationship("Joke",
                            backref="user",
                            lazy="joined")

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password + self.salt)

    def set_password(self, password, pubkey, privkey):
        self.privkey_1 = privkey
        self.pubkey_1 = pubkey
        self.salt = secrets.token_hex(8)
        self.password_hash = bcrypt.generate_password_hash(password + self.salt).decode("ascii")

        cipher = CAST.new(password.encode("utf8"), CAST.MODE_ECB)
        pubkey = pubkey + "0000000000000000000000"
        privkey = privkey + "00000000000000"
        self.pubkey = cipher.encrypt(pubkey.encode("utf8"))
        self.privkey = cipher.encrypt(privkey.encode("utf8"))

        db.session.add(self)
        db.session.commit()

    # It is very-very safe.
    def get_keys(self, password):
        return self.pubkey_1, self.privkey_1 
# cipher = CAST.new(password.encode("utf8"), CAST.MODE_ECB)
        #return cipher.decrypt(self.pubkey).decode("utf8")[:-22], cipher.decrypt(self.privkey).decode("utf8")[:-14]

    def get_keys_unsafe(self):
        return self.pubkey_1, self.privkey_1

    @staticmethod
    def get(user_id=None, username=None, email=None):
        if user_id:
            return User.query.get(id=user_id)
        if username:
            return User.query.filter_by(username=username).first()
        if email:
            return User.query.filter_by(email=email).first()
        return User.query.all()
