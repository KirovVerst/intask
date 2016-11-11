from __future__ import absolute_import, unicode_literals
from celery import shared_task
from intask.settings import EMAIL_SETTINGS

import requests


@shared_task
def send_simple_message(to_address):
    r = requests.post(
        "https://api.mailgun.net/v3/{0}/messages".format(EMAIL_SETTINGS['domain_name']),
        auth=("api", EMAIL_SETTINGS['api_key']),
        data={"from": "Intask <{0}>".format(EMAIL_SETTINGS['address']),
              "to": [to_address],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!"})
    return dict(code=r.status_code)
