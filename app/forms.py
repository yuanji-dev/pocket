from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User


class LoginForm(Form):
    #length?
    #add remember me option.
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='wrong email.')])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='wrong email.')])
    #todo add re check.
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password',
                             validators=[Required(), EqualTo('repassword', message='Passwords dont match.')])
    repassword = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email has been registered.')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username has been registered.')


#todo link regex
class AddItemForm(Form):
    link = StringField('Link', validators=[Required()])
    submit = SubmitField('Add')