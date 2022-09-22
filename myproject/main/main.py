import datetime

from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user
from markupsafe import Markup

from myproject import db
from myproject.main.forms import RegistrationForm, LoginForm
from myproject.models import UsersModel

main = Blueprint('main', __name__, template_folder="temp", )


@main.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("messaging.chating"))

    form = LoginForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True, duration=datetime.timedelta(weeks=52))

            nex = request.args.get('next')

            if nex is None or not nex[0] == '/':
                nex = '/'
            return redirect(nex)
        else:
            flash(Markup('''<div class="alert alert-primary alert-dismissible fade show" style="margin: 0;" 
              role="alert"> The password or the email is incorrect.  </div>'''))
            return render_template("login.html", form=form, d=form.errors)
    print(form.errors)

    return render_template('login.html', form=form)


@main.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect('/chats')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(email=form.email.data).first()
        if user:
            flash(Markup('This email already exist try <a href="/login">login </a> instead'))
            return render_template('register.html', form=form, d=form.errors)

        user = UsersModel(email=form.email.data, username=form.username.data,
                          password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)
