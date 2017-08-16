import requests
from celery import shared_task
from intask.settings import EMAIL_SETTINGS


@shared_task
def send_message(subject, text, recipient=None):
    if recipient is None:
        recipient = EMAIL_SETTINGS['address']

    response = requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(EMAIL_SETTINGS['domain_name']),
        auth=("api", EMAIL_SETTINGS['api_key']),
        data={
            "from": "Intask Administration <{}>".format(EMAIL_SETTINGS['address']),
            "to": [recipient],
            "subject": subject,
            "text": text
        })
    try:
        return response.json()
    except Exception as e:
        return {'message': e}
