from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired, EqualTo ,ValidationError
from treasure.models import User ,Questions

class LoginForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Login')

    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user == None:
            raise ValidationError('Username not registered , Please Sign Up ')


class RegistrationForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Sign Up')

    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one')

    def validate_email(self,email):
        email= User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already registered.')

class Answer(FlaskForm):
    answer=StringField('Answer:', validators=[DataRequired()])
    submit= SubmitField('Submit Answer')



