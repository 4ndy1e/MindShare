from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app import db
import sqlalchemy as sa
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length


class LoginForm(FlaskForm):
  # these fields are ready to be placed into HTML, so we dont have to build HTML elements like usual
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Rememebr me')
  submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')
  
  def validate_username(self,username):
    user = db.session.scalar(sa.select(User).where(User.username == username.data))
    
    if user is not None:
      raise ValidationError('Please use a different username')
    
  def validate_email(self,email):
    user = db.session.scalar(sa.select(User).where(User.email == email.data))
    
    if user is not None:
      raise ValidationError('Please use a different email address')


class EditProfileForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
  submit = SubmitField('Submit')
  