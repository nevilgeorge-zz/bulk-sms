# views.py
from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user = {'name': 'Nevil'}
	return render_template(
		'index.html',
		hackathon='Wildhacks',
		user=user
	)
