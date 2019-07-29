from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from .config import Config

app = Flask(__name__, template_folder="../../templates", static_folder="../../static", static_url_path="/static")
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from .controllers import index, joke, auth, errorhandlers, service
from .models.User import User
from .models.joke import Joke, Likes
