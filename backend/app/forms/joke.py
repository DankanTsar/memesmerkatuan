from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, PasswordField
from wtforms.validators import Length, DataRequired, ValidationError
from ..misc.cur_user import cur_user


def match(form, field):
    user = None
    if cur_user():
        user = cur_user()
    if not user.check_password(field.data):
        raise ValidationError("Неправильный пароль")


class JokeForm(FlaskForm):
    joke_text = TextAreaField('Ваша шутка', validators=[DataRequired(message='Поле не должно быть пустым'),
                                                        Length(min=5, max=250,
                                                               message='Текст должен быть не '
                                                                       'меньше 5 и не больше 250 символов')])
    joke_password = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий'),
                                                        match])
    joke_submit = SubmitField('Отправить')
