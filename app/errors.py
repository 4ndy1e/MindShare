from app import app, db
from flask import render_template

@app.errorhandler(404)
def not_found_handler(error):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  # rollback to reset db back to clean state
  db.session.rollback()
  return render_template('500.html'), 500