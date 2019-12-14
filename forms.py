from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, TextAreaField

class LoginForm(FlaskForm):
    username = StringField('Username', id="luname", validators=[validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('New Password', id="lpword", validators= [validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', id="runame",validators=[validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('New Password', id="rpword", validators=[validators.DataRequired()])


class ThreadForm(FlaskForm):
    title = StringField("Title", id="title", validators=[validators.DataRequired()])
    # Can you text area.
    body = StringField("Message", id="message", validators=[validators.DataRequired()])


class QueryForm(FlaskForm):
    query_id = StringField('Query Id', id="userquery", validators=[validators.DataRequired()])


class LoggerForm(FlaskForm):
    user_id = StringField('User Id', id="userid", validators=[validators.DataRequired()])


