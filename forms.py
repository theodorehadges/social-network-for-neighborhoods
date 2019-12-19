from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, TextAreaField, HiddenField, SubmitField, SelectField


class LoginForm(FlaskForm):
    username = StringField('Username', id="luname", validators=[validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('New Password', id="lpword", validators= [validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', id="runame", validators=[validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('New Password', id="rpword", validators=[validators.DataRequired()])


class ThreadForm(FlaskForm):
    title = StringField("Title", id="title", validators=[validators.DataRequired()])
    # Can you text area.
    body = StringField("Message", id="message", validators=[validators.DataRequired()])


class SearchForm(FlaskForm):
    #search_types = ["All threads, Friends, Neighborhood, Block"]
    search_type = SelectField("Search Type", choices = [("all",
    "All Threads"), ("friends", "Friends"), ("neighbor", "Neighbor"), \
            ("neighborhood", "Neighborhood"), ("block", "Block")], \
            validators = [validators.DataRequired()])
    search_text = StringField("Search Text", id="search_text", validators=[validators.DataRequired()])

class QueryForm(FlaskForm):
    query_id = StringField('Query Id', id="userquery", validators=[validators.DataRequired()])


class LoggerForm(FlaskForm):
    user_id = StringField('User Id', id="userid", validators=[validators.DataRequired()])


class FriendAcceptForm(FlaskForm):
    request_id = HiddenField()
    request_accept = SubmitField('Accept')
    request_remove = SubmitField('Remove')

class FriendRequestForm(FlaskForm):
    request_id = HiddenField()
    request_invite = SubmitField('Invite')


class MessageForm(FlaskForm):
    thread_id = HiddenField()
    title = StringField("Title", id="title", validators=[validators.DataRequired()])
    body = StringField("Message", id="message", validators=[validators.DataRequired()])