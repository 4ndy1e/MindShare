from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import sqlalchemy as sa
from urllib.parse import urlsplit


@app.route('/')
@app.route('/index')
@login_required
def index():
  # dummy data
  user = {"username" : "Andy"}
  posts = [
    {
      'author': {'username': 'Luan'},
      'body': 'I like this post!'
    },
    {
      'author': {'username': 'Hieu'},
      'body': 'I am a sophomore student.'
    }
  ]

  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated: 
    return redirect(url_for('index'))

  # loginform class
  form = LoginForm()

  # form.validate_on_submit() sends GET request to receieve the web p;age with the form, which returns false 
  if form.validate_on_submit():
    # user enters valid data after POST request pressing submit button
    user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')

    if not next_page or urlsplit(next_page).netloc != '':
      next_page = url_for('index')
      
    return url_for(next_page)

  return render_template('login.html', title="Sign In", form=form)

@app.route('logout')
def logout():
  logout_user()
  return redirect(url_for('index'))
