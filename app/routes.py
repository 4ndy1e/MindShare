from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
  # loginform class
  form = LoginForm()

  # form.validate_on_submit() sends GET request to receieve the web p;age with the form, which returns false 
  if form.validate_on_submit():
    # user enters valid data after POST request pressing submit button
    flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
    return redirect(url_for('index'))

  return render_template('login.html', title="Sign In", form=form)
