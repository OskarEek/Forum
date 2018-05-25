from wtforms import SubmitField, TextField, TextAreaField, Form, BooleanField, StringField, PasswordField
from wtforms.validators import Required, DataRequired, Length, EqualTo
from flask_wtf import FlaskForm


class AddItemForm(FlaskForm):
    title = TextField('Titel', validators=[Required()])
    description = TextAreaField('Diskutions-ämne, fråga...')
    submit = SubmitField('Lägg till')

class RegisterUserForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=3, max=20)])
    password = PasswordField('New Password',
        validators= [DataRequired(), EqualTo('confirm', message = 'Password must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=3, max=20)])
    password = PasswordField('Password', validators= [DataRequired()])
    submit = SubmitField('Log-In')
