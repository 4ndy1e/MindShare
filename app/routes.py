from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import sqlalchemy as sa
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app.forms import EditProfileForm

@app.before_request
def before_request():
  if current_user.is_authenticated: 
    current_user.last_seen = datetime.now(timezone.utc)
    db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
  # dummy data
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

  return render_template('index.html', title='Home', posts=posts)

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

    return redirect(next_page)

  return render_template('login.html', title="Sign In", form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated: 
    return redirect(url_for('index'))

  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)

    db.session.add(user)
    db.session.commit()

    flash('Congratulations, you are now registered!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
  # similar to scalar() but raises 404 instead of None
  user = db.first_or_404(sa.select(User).where(User.username == username))

  # fake posts
  posts = [
    {'author' : user, 'body' : 'Test post #1'},
    {'author' : user, 'body' : 'Test post #2'}
  ]

  return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm()

  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    
    db.session.commit()
    flash('Your changes have been saved!')
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    # prepopulate fields with the data that is current stored in db
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me

  return render_template('edit_profile.html', form=form, title='Edit Profile')

