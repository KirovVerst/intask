import requests
from intask.settings import EMAIL_SETTINGS


def send_simple_message(to_address):
    return requests.post(
        "https://api.mailgun.net/v3/{0}/messages".format(EMAIL_SETTINGS['domain_name']),
        auth=("api", EMAIL_SETTINGS['api_key']),
        data={"from": "Intask <{0}>".format(EMAIL_SETTINGS['address']),
              "to": [to_address],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!"})
