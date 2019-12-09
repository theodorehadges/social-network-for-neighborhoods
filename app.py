import datetime
import subprocess

import flask
import sqlalchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegistrationForm, LoginForm

from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

from models import User

app.config['SECRET_KEY'] = 'FAKE KEY FOR CI/CD'
db.create_all()
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index_page():
    if current_user:
        return redirect("")
    else:
        return render_template("register_login.html")
    return render_template("index.html")


#https://flask.palletsprojects.com/en/1.0.x/patterns/wtforms/
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        bcrypt_hash = bcrypt.generate_password_hash(password=password)
        try:
            user = User(name=form.username.data, password_hash=bcrypt_hash)
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return '<div id="success">failure</div>'
        print("succeeded render success back")
        return '<div id="success">success</div>'
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if validate_user(username, password):
            return '<div id="result">Success</div>'
        return '<div id="result">Incorrect</div>'
    return render_template('login.html', form=form)


def validate_user(username, password):
    found_user = User.query.filter_by(name=username).first()
    if found_user:
        return bcrypt.check_password_hash(found_user.password_hash, password)
    return False


@app.route("/logout")
@login_required
def logout():
    last_log = current_user.log_logs[-1]
    logout_user()
    last_log.logout_time = datetime.datetime.now()
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
