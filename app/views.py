# views.py
from app import app
from flask import flash, render_template
from forms import SendMessageForm

@app.route('/')
@app.route('/index')
def index():
	"""Render index page."""
	user = {'name': 'Nevil'}
	return render_template(
		'index.html',
		hackathon='Wildhacks',
		user=user
	)


@app.route('/send', methods=['GET', 'POST'])
def send():
	"""Render sms sending page."""
	send_message_form = SendMessageForm()
	if send_message_form.validate_on_submit():
		flash('Message sending!')

	return render_template(
		'send.html',
		form=send_message_form
	)


@app.route('/add')
def add():
	"""Render add number/ add by file page."""
	return render_template(
		'add.html'
	)
