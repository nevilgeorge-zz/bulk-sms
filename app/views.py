# views.py
import datetime
import os

from flask import flash, redirect, render_template

from app import app, db, models, utils, repository
from app.exceptions.duplicate_error import DuplicateError
from app.repository import message_repo, number_repo, sender_repo, subscription_repo
from app.twilio_dispatcher import TwilioDispatcher
import forms

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
	"""Render index page."""

	return render_template(
		'index.html',
		hackathon='Wildhacks'
	)


@app.route('/send', methods=['GET', 'POST'])
def send():
	"""Render sms sending page."""

	send_message_form = forms.SendMessageForm()
	if send_message_form.validate_on_submit():
		# check if there are any active senders first
		senders = sender_repo.get_all()
		if len(senders) == 0:
			# fail early if no senders
			flash('No senders added!', 'error')
			return redirect('/send')

		subscription_id = int(send_message_form.subscription.data)
		message_text = send_message_form.message_text.data

		# create Message entity
		message_repo.create_one(
			text=message_text,
			sent_at=datetime.datetime.utcnow(),
			subscription_id=subscription_id
		)

		twilio_dispatcher = TwilioDispatcher()
		failed = twilio_dispatcher.send_to_subscription(subscription_id, message_text)

		if len(failed) != 0:
			flash('Following numbers failed to be sent to:', 'error')
			for number, exception in failed.iteritems():
				flash('{num} : {reason}'.format(
					num=number,
					reason=exception
				), 'error')

		send_message_form.message_text.data = None
		send_message_form.subscription.data = None

	messages = message_repo.get_all()

	return render_template(
		'send.html',
		messages=messages,
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
			number_repo.create_one(
				number=normalized_number,
				subscription_id=int(add_number_form.subscription.data)
			)
			flash('Number added!', 'success')
		except DuplicateError as e:
			print e
			flash('Number already exists!', 'error')
			pass

		# reset form
		add_number_form.number.data = None
		add_number_form.subscription.data = '1'

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
				number_repo.create_one(
					number=num,
					subscription_id=subscription_id
				)
			except DuplicateError as e:
				flash(
					'Number {number} already exists!'.format(number=e.number),
					'error'
				)
				print e
				pass

		flash('Numbers added!', 'success')

	return render_template(
		'number.html',
		add_number_form=add_number_form,
		upload_file_form=upload_file_form
	)


@app.route('/sender', methods=['GET', 'POST'])
def sender():
	"""Render show senders/ add sender page."""

	add_sender_form = forms.AddSenderForm()

	if add_sender_form.validate_on_submit():
		number = utils.normalize_number(add_sender_form.sender_number.data)
		try:
			sender_repo.create_one(
				number=number
			)

			# check for numbers with no sender_id
			sender = sender_repo.get_min_sender()
			numbers = number_repo.get_many_by_kwargs(
				sender_id=None
			)
			for number in numbers:
				number.sender_id = sender.id
				db.session.add(number)
			db.session.commit()

			flash('Sender added!', 'success')
		except DuplicateError as e:
			flash('Sender already exists!', 'error')
			print e
			pass

		# reset form
		add_sender_form.sender_number.data = None

	senders = sender_repo.get_all()

	return render_template(
		'sender.html',
		senders=senders,
		add_sender_form=add_sender_form
	)


@app.route('/sender/<sender_id>', methods=['GET'])
def sender_views(sender_id):
	"""Render all numbers associated with given sender."""
	sender = sender_repo.get_by_id(sender_id)
	if sender == None:
		flash('Sender does not exist!', 'error')
		return redirect('/')

	numbers = number_repo.get_many_by_kwargs(
		sender_id=sender_id
	)

	return render_template(
		'sender_views.html',
		numbers=numbers
	)


@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
	"""Render show/create subscriptions page."""

	add_sub_form = forms.AddSubscriptionForm()
	if add_sub_form.validate_on_submit():
		try:
			subscription_repo.create_one(
				title=add_sub_form.title.data
			)
			flash('Subscription added!', 'success')
		except DuplicateError as e:
			flash('Subscription already exists!', 'error')
			print e
			pass

		# reset form
		add_sub_form.title.data = None

	subscriptions = subscription_repo.get_all()

	return render_template(
		'subscription.html',
		subscriptions=subscriptions,
		add_sub_form=add_sub_form
	)


@app.route('/subscription/<sub_id>', methods=['GET'])
def subscription_view(sub_id):
	"""Render all numbers in given subscription."""
	subscription = subscription_repo.get_by_id(sub_id)
	if subscription == None:
		flash('Subscription does not exist!', 'error')
		return redirect('/')

	numbers = number_repo.get_many_by_kwargs(
		subscription_id=sub_id
	)

	return render_template(
		'subscription_views.html',
		numbers=numbers
	)
