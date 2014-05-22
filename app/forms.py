from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User


class LoginForm(Form):
    #length?
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='wrong email.')])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log in')

