# views.py
from app import app, models
from flask import redirect, render_template
import forms

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

	send_message_form = forms.SendMessageForm()
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


@app.route('/number', methods=['GET', 'POST'])
def number():
	"""Render add number/ add by file page."""

	to_number_form = forms.AddToNumberForm()
	upload_file_form = forms.UploadFileForm()

	if to_number_form.validate_on_submit():
		if to_number_form.to_number.data != '':
			print 'To number'
			print to_number_form.to_number.data

	if upload_file_form.validate_on_submit():
		print upload_file_form.number_file.data

	return render_template(
		'add.html',
		to_number_form=to_number_form,
		from_number_form=from_number_form,
		upload_file_form=upload_file_form
	)


@app.route('/sender', methods=['GET', 'POST'])
def sender():
	"""Render show senders/ add sender page."""

	sender_list = models.Sender.query.all()
	senders = [sender.sender_number for sender in sender_list]

	add_sender_form = forms.AddSenderForm()

	if add_sender_form.validate_on_submit():
		print add_sender_form.sender_number.data

	return render_template(
		'sender.html',
		senders=senders,
		add_sender_form=add_sender_form
	)
