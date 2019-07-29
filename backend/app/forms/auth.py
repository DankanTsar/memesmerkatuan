import re
from ..models.User import User
from ..misc.cur_user import cur_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, ValidationError, Email


def exist(form, field):
    if User.get(username=field.data):
        raise ValidationError("Такой пользователь уже существует")


def email_exist(form, field):
    if User.get(email=field.data):
        raise ValidationError("Такой email уже существует")


def not_exist(form, field):
    if User.get(username=field.data) is None:
        raise ValidationError("Такого пользователя не существует")


def check_correct_name(form, field):
    if not re.match(r'[a-zA-Z0-9_]', field.data):
        raise ValidationError("В имени пользователя могут быть только цифры, латинские буквы и нижние подчёркивания")


def match(form, field):
    user = None
    if cur_user():
        user = cur_user()
    elif form.username_log.data is not '':
        user = User.get(username=form.username_log.data)
    if user and not user.check_password(field.data):
        raise ValidationError("Неправильный пароль")


class RegForm(FlaskForm):
    username_reg = StringField("Имя пользователя", validators=[Length(5, message='Логин слишком короткий'),
                                                               exist, check_correct_name])
    email_reg = StringField("E-MAIL пользователя", validators=[Length(5, message='Логин слишком короткий'),
                                                               email_exist, check_correct_name])

    password_reg = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий')])
    confirm_reg = PasswordField("Повторите пароль",
                                validators=[Length(8, message='Пароль слишком короткий'),
                                            EqualTo("password_reg", message="Пароли должны совпадать")])
    pubkey_reg = StringField("Публичный ключ",  # TODO make pubkey verification
                             validators=[Length(8, message='Публичный ключ слишком короткий')])
    privkey_reg = StringField("Приватный ключ",  # TODO make privkey verification
                              validators=[Length(8, message='Приватный ключ слишком короткий')])
    submit_reg = SubmitField("Зарегистрироваться")


class LogForm(FlaskForm):
    username_log = StringField("Имя пользователя", validators=[Length(5, message='Логин слишком короткий'),
                                                               check_correct_name, not_exist])
    password_log = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий'),
                                                       match])
    submit_log = SubmitField("Войти")
