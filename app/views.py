# views.py
from app import app
from flask import redirect, render_template
from forms import AddToNumberForm, AddFromNumberForm, SendMessageForm, UploadFileForm

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
		print 'Sent message {message_text} to:'.format(
			message_text=send_message_form.message_text.data
		)
		print send_message_form.subscriptions.data
		return redirect('/index')

	return render_template(
		'send.html',
		form=send_message_form
	)


@app.route('/add', methods=['GET', 'POST'])
def add():
	"""Render add number/ add by file page."""

	to_number_form = AddToNumberForm()
	from_number_form = AddFromNumberForm()
	upload_file_form = UploadFileForm()

	if to_number_form.validate_on_submit():
		if to_number_form.to_number.data != '':
			print 'To number'
			print to_number_form.to_number.data

	if from_number_form.validate_on_submit():
		if from_number_form.from_number.data != '':
			print 'From number'
			print from_number_form.from_number.data

	if upload_file_form.validate_on_submit():
		print upload_file_form.number_file.data

	return render_template(
		'add.html',
		to_number_form=to_number_form,
		from_number_form=from_number_form,
		upload_file_form=upload_file_form
	)
