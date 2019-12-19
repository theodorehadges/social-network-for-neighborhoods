import datetime
import subprocess

import flask
import flask_login
import sqlalchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


from forms import RegistrationForm, LoginForm, ThreadForm, FriendRequestForm, FriendAcceptForm, SearchForm
from models import *
from util import make_thread_message_into_thread

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)




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
    if current_user.is_authenticated:
        return redirect("/feeds")
    lform = LoginForm(request.form)
    rform = RegistrationForm(request.form)
    return render_template("register_login.html", lform=lform, rform=rform)


@app.route('/feeds')
@login_required
def feeds():
    current_user.id = 4 # for debugging
    #friend_thread = get_thread_friend_unread(current_user.id)
    #messages_by_thread = make_thread_message_into_thread(friend_thread)
    friend_messages = get_recent_friend_messages(current_user.id)
    neighbor_messages = get_recent_neighbor_messages(current_user.id)
    neighborhood_messages = get_recent_neighbor_messages(current_user.id)
    block_messages = get_recent_block_messages(current_user.id)
    
    return render_template("feeds.html", friend_messages=friend_messages,
            neighbor_messages=neighbor_messages,
            neighborhood_messages=neighborhood_messages,
            block_messages=block_messages)

    #return "yay"


@app.route('/thread', methods=['GET', 'POST'])
@login_required
def thread():
    form = ThreadForm(request.form)
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        thread_id = make_thread(current_user.id, title, body)
        return redirect("/thread/{}".format(thread_id))
    return render_template("thread.html", tform=form)


@app.route('/thread/<int:thread_id>')
@login_required
def get_thread(thread_id):
    #messages = get_messages_by_thread_id(thread_id)
    messages = get_messages_by_thread_id(2)

    print(messages)
    return "yay"

@app.route('/thread/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm(request.form)

    if form.validate_on_submit():
        search_type = form.search_type.data
        search_text = form.search_text.data
        search_results = search_threads(current_user.id, search_type, search_text)
        print(search_results)
        return render_template("display_threads.html", threads=search_results)
    return render_template("search.html", tform=form)
   


@app.route('/possible_friends', methods=['GET', 'POST'])
@login_required
def possible_friends():
    form = FriendRequestForm(request.form)
    users = get_user_list(current_user.id)
    if form.validate_on_submit():
        friend_id = form.request_id.data
        make_request_record(current_user.id, friend_id)
        return redirect("feeds")
    return render_template("possible_friends.html", form=form, users=users)


@app.route('/pending_friends', methods=['GET', 'POST'])
@login_required
def pending_friends():
    form = FriendAcceptForm(request.form)
    pfriends = get_pending_friends(current_user.id)
    if form.validate_on_submit():
        r_id = form.request_id.data
        if form.request_accept.data:
            update_request_friends(current_user.id, r_id, True)
        else:
            update_request_friends(current_user.id, r_id, False)
        return redirect('friends')
    return render_template("pending_friends.html", form=form, users=pfriends)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        bcrypt_hash = bcrypt.generate_password_hash(password=password)
        try:
            print(bcrypt_hash)
            user = User(username=form.username.data, password=bcrypt_hash)
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user)
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            return '<div id="success">failure</div>'
        return redirect('/feeds')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if validate_user(username, password):
            found_user = User.query.filter_by(username=username).first()
            flask_login.login_user(found_user)
            return redirect('/feeds')
        return '<div id="result">Incorrect</div>'
    return render_template('login.html', form=form)


def validate_user(username, password):
    found_user = User.query.filter_by(username=username).first()
    if found_user:
        return bcrypt.check_password_hash(found_user.password, password)
    return False



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
