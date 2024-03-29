from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, TextAreaField, HiddenField, SubmitField, \
    SelectField, SelectMultipleField
from wtforms.validators import Required
from wtforms.widgets import CheckboxInput, ListWidget


class LoginForm(FlaskForm):
    username = StringField('Username', id="luname", validators=[validators.DataRequired()])
    password = PasswordField('Password', id="lpword", validators= [validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', id="runame", validators=[validators.DataRequired()])
    password = PasswordField('New Password', id="rpword", validators=[validators.DataRequired()])
    firstname = StringField('First Name', id="rfname", validators=[validators.DataRequired()])
    lastname = StringField('Last Name', id="rlname", validators=[validators.DataRequired()])
    email = StringField("Email", id="email", validators=[validators.DataRequired()])
    street = StringField("Street", id="street", validators=[validators.DataRequired()])
    city = StringField("City", id="city", validators=[validators.DataRequired()])
    zipcode = StringField("Zipcode", id="zipcode", validators=[validators.DataRequired()])
    state = StringField("State", id="state", validators=[validators.DataRequired()])
    description = StringField("Bio", id="bio", validators=[validators.DataRequired()])

class ThreadForm(FlaskForm):
    title = StringField("Title", id="title", validators=[validators.DataRequired()])
    # Can you text area.
    body = StringField("Message", id="message", validators=[validators.DataRequired()])
    make_type = SelectField("Make Thread Type", choices=[("neighborhood", "Neighborhood"), ("block", "Block")])

class MultiCheckboxField(SelectMultipleField):
    widget			= ListWidget(prefix_label=False)
    option_widget	= CheckboxInput()


class ThreadUserForm(FlaskForm):
    title = StringField("Title", id="title", validators=[validators.DataRequired()])
    body = StringField("Message", id="message", validators=[validators.DataRequired()])
    # user_choice = SelectMultipleField("Pick Users to start group", choices=[])
    user_choice = MultiCheckboxField('Please select users you want to have a conversation with',
                                     choices=[])


class SearchForm(FlaskForm):
    #search_types = ["All threads, Friends, Neighborhood, Block"]
    search_type = SelectField("Search Type", choices=[("all",
    "All Threads"), ("friend", "Friends"), ("neighbor", "Neighbor"), \
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


class Neighborhood(FlaskForm):
    neighborhood_type = SelectField("Neighborhood Type", coerce=int, id="neighborhoodid", choices=[], validators=[validators.DataRequired()])
    block_type = SelectField("Block Type", id="blockid", coerce=int, choices=[], validators=[validators.DataRequired()])
