import datetime
import subprocess

import flask
import flask_login
import sqlalchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, flash, render_template, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegistrationForm, LoginForm, ThreadForm, FriendRequestForm, FriendAcceptForm, SearchForm, MessageForm, \
    Neighborhood
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
    return render_template("login.html", lform=lform)

@app.route('/profile/<int:profile_id>')
@login_required
def profile_page(profile_id):
    # show friends on map
    # show neighbors on map
    friends = get_all_friends(profile_id) # Change param to curent_user.id 
    #neighbors = get_all_neighbors(current_user.id)
    userprofile = get_profile_info_from_uid(profile_id) 
   
    return render_template("profile.html", friends=friends, userprofile=userprofile)


@app.route('/feeds')
@login_required
def feeds():
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



@app.route('/thread', methods=['GET', 'POST'])
@login_required
def thread():
    form = ThreadForm(request.form)
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        type = form.search_type.data
        thread_id = make_thread(current_user.id, title, body, type)
        return redirect("/thread/{}".format(thread_id))
    return render_template("thread.html", tform=form)


@app.route('/thread/<int:thread_id>')
@login_required
def get_thread(thread_id):
    form = MessageForm()
    messages = get_messages_by_thread_id(thread_id)
    return render_template("thread_message.html", form=form, messages=messages, thread_id=thread_id)


@app.route('/message/reply', methods=['POST'])
@login_required
def message_reply():
    form = MessageForm(request.form)
    if form.validate_on_submit():
        thread_id = form.thread_id.data
        title = form.title.data
        message = form.body.data
        message_id = insert_message_reply(thread_id, current_user.id, title, message)
        insert_message_read(message_id, thread_id, current_user.id)
        update_message_read(message_id, thread_id, current_user.id)
        return redirect('/thread/{}'.format(thread_id))

@app.route('/thread/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm(request.form)

    if form.validate_on_submit():
        search_type = form.search_type.data
        search_text = form.search_text.data
        search_results = search_threads(current_user.id, search_type, search_text)
        print(search_results)
        return render_template("search_results.html", threads=search_results)
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


@app.route('/possible_neighbors', methods=['GET', 'POST'])
@login_required
def possible_neighbors():
    form = FriendRequestForm(request.form)
    users = get_user_list(current_user.id)
    if form.validate_on_submit():
        friend_id = form.request_id.data
        insert_into_neighbors(current_user.id, friend_id)
        return redirect("feeds")
    return render_template("possible_friends.html", form=form, users=users)

@app.route('/friends')
@login_required
def get_friends():
    users = get_all_friends(current_user.id)
    return render_template("friends.html", users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        bcrypt_hash = bcrypt.generate_password_hash(password=password)
        lat_lon = get_lat_lon_from_address(form.street.data, form.city.data,
                form.state.data)
        try:
            insert_user(form, bcrypt_hash, lat_lon['lat'], lat_lon['lng'])
            found_user = User.query.filter_by(username=form.username.data).first()
            flask_login.login_user(found_user)
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            return '<div id="success">Registration unsuccessful. Please try \
        a different username.</div>'
        return redirect('/neighborhood')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm(request.form)
    if request.method == 'POST' and lform.validate():
        username = lform.username.data
        password = lform.password.data
        if validate_user(username, password):
            found_user = User.query.filter_by(username=username).first()
            flask_login.login_user(found_user)
            return redirect('/feeds')
        return '<div id="result">Incorrect</div>'
    return render_template('login.html', lform=lform)


def validate_user(username, password):
    found_user = User.query.filter_by(username=username).first()
    if found_user:
        return bcrypt.check_password_hash(found_user.password, password)
    return False


@app.route('/block')
@login_required
def blocks():
    neighborhood_id = request.args.get('n_ida')
    blocks = get_blocks(neighborhood_id)
    block_list = [[str(id), name] for id, name in blocks]
    block_dict = {"blocks": block_list}
    return jsonify(block_dict)


@app.route('/neighborhood', methods=['GET', 'POST'])
@login_required
def neighborhood():
    form = Neighborhood(request.form)
    neighborhoods = get_neighborhoods()
    neighbor_list = [(id, name) for id, name in neighborhoods]
    blocks = get_blocks(neighbor_list[0][0])
    block_list = [(id, name) for id, name in blocks]
    form.neighborhood_type.choices = neighbor_list
    form.block_type.choices = block_list
    # need to skip validating because we change form values on front end
    if flask.request.method == 'POST':
        block_id = form.block_type.data
        neighborhood_id = form.neighborhood_type.data
        potential_neighbors = get_neighbors_from_block(current_user.id, block_id)
        potential_neighbors_list = [x for x in potential_neighbors]
        # if there are people in a block already insert into block apply otherwise auto insert into block
        if potential_neighbors_list:
            insert_into_block_apply(current_user.id, block_id)
        else:
            update_block_on_uid(current_user.id, block_id)
        return redirect("/feeds")
    return render_template("neighborhood.html", form=form)

@app.route('/pending_block_approval', methods=['GET', 'POST'])
@login_required
def pending_block_approval():
    form = FriendAcceptForm(request.form)
    pneighbor = get_pending_block_approvals(current_user.id)
    if form.validate_on_submit():
        r_id = form.request_id.data
        if form.request_accept.data:
            update_block_approval(current_user.block_id, r_id, current_user.id, True)
        else:
            update_block_approval(current_user.block_id, r_id, current_user.id, False)
        return redirect('feeds')
    return render_template("pending_friends.html", form=form, users=pneighbor)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
