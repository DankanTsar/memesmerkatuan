import os
import unittest
from wtforms import StringField, SubmitField
from backend import db, app
from backend.models.joke import Joke
from backend.forms.joke import JokeForm


TEST_DB = 'test.sqlite'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseTestModelSuite(unittest.TestCase):
    def setUp(self):
        app.config['SECRET_KEY'] = "TestKey"
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.joke = Joke("Sample text", 1)
        self.joke.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModelJoke(BaseTestModelSuite):
    def test_should_has_needed_fields(self):
        self.assertTrue(hasattr(self.joke, "text"))
        self.assertTrue(hasattr(self.joke, "user_id"))

    def test_is_remove_joke_method_works(self):
        test_id = self.joke.joke_id
        self.joke.remove_joke()
        self.assertIsNone(Joke.query.get(test_id))

    def test_is_get_text_method_works(self):
        self.assertEqual(self.joke.get_text(), "Sample text")

    def test_is_change_text_method_works(self):
        self.joke.change_text("New sample text")
        self.assertEqual(self.joke.get_text(), "New sample text")


class TestJokeForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = JokeForm()

    def tearDown(self):
        del self.form

    def test_should_has_needed_fields(self):
        self.assertTrue(hasattr(self.form, "joke_text"))
        self.assertTrue(hasattr(self.form, "joke_submit"))

    def test_should_joke_text_field_is_string_field(self):
        self.assertIsInstance(self.form.joke_text, StringField)

    def test_should_joke_submit_field_is_string_field(self):
        self.assertIsInstance(self.form.joke_submit, SubmitField)
