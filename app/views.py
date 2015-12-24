# views.py
import os

from flask import redirect, render_template
from sqlalchemy.exc import IntegrityError

from app import app, db, models, utils, repository
from app.repository import number_repo
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

	add_number_form = forms.AddNumberForm()
	upload_file_form = forms.UploadFileForm()

	if add_number_form.validate_on_submit():
		normalized_number = utils.normalize_number(add_number_form.number.data)
		try:
			number_repo.create_number(
				number=normalized_number,
				subscription_id=int(add_number_form.subscription.data)
			)
		except IntegrityError:
			print 'Number already exists!'
			pass

	if upload_file_form.validate_on_submit():
		f = upload_file_form.number_file.data
		subscription_id = int(upload_file_form.subscription.data)
		extension = os.path.splitext(f.filename)[1]

		if extension == '.csv':
			numbers = utils.read_from_csv_file(f)
		elif extension == '.txt':
			numbers = utils.read_from_txt_file(f)

		for num in numbers:
			try:
				number_repo.create_number(
					number=num,
					subscription_id=subscription_id
				)
			except IntegrityError:
				print '{num} already exists!'.format(num=num)
				pass

	return render_template(
		'number.html',
		add_number_form=add_number_form,
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
