from flask import redirect, render_template, session, url_for
from ..models.Web3Provider import Merkatuan, send_payable_transaction, w3
from .. import app
from ..forms.auth import RegForm, LogForm
from ..models.User import User
from ..misc.cur_user import cur_user
import binascii



@app.route('/registration', methods=['GET', 'POST'])
def reg():
    """
    Отвечает за вывод страницы регистрации и регистрацию
    :return: Страница регистрации
    """

    form = RegForm()

    if form.validate_on_submit():
        user = User(form.username_reg.data, form.email_reg.data)
        user.set_password(form.password_reg.data,
                          form.pubkey_reg.data, form.privkey_reg.data)
        session["Username"] = user.username
        try:
            send_payable_transaction(Merkatuan.functions.transfer(form.pubkey_reg.data, 10000000000000000000)
                                     .buildTransaction(dict(gas=3000000)),
                                     app.config.get('TEST_PUBLIC_KEY'), app.config.get('TEST_PRIVATE_KEY'))
        except BaseException as e:
            print('FUCK', e, form.pubkey_reg.data, type(form.pubkey_reg.data))
        return redirect(url_for("index"))

    return render_template('auth/registration.html', form=form, user=cur_user())


@app.route('/login', methods=['GET', 'POST'])
def log():
    """
    Отвечает за вывод страницы входа и вход
    :return: Страница входа
    """

    form = LogForm()

    if form.validate_on_submit():
        session["Username"] = form.username_log.data
        return redirect(url_for("index"))

    return render_template('auth/login.html', form=form, user=cur_user())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Username' in session:
        session.pop('Username')
    return redirect('/')
