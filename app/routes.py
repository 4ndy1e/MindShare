from flask import render_template
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

@app.route('/login')
def login():
  # loginform class
  form = LoginForm()

  return render_template('login.html', title="Sign In", form=form)
