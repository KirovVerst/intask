# coding=utf-8
from django.core.mail import send_mail, BadHeaderError


def invite_user_to_event(sender, recipient, event):
	sender_text = "From: "
	if sender.first_name and sender.last_name:
		sender_text += sender.first_name + " " + sender.last_name + "(" + sender.email + ")"
	else:
		sender_text += sender.email

	url = "http://127.0.0.1:8000/register"

	event_text = "Invitation to : Event \"" + event.title + "\""

	subject = "InTask : Invitation to Event"

	message = sender_text + "<br>" + event_text + "<br><br>" \
			  + unicode("Registration : ") + url

	try:
		send_mail(subject, "", sender.email, [recipient], html_message=message)
		return True
	except BadHeaderError:
		return False
