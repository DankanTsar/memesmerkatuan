import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    WEB3_HTTP_PROVIDER_ADDRESS = "https://kovan.infura.io/v3/c5e971595b51485c904f05a9ffef2336"
    MEMESMERKATUAN_ADDRESS = "0x3E60136b78FA890323D9845a4765B497f5b47484"
