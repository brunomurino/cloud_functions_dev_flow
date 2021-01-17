import requests
import json
import os

from google.cloud import (
    secretmanager,
    bigquery,
    storage,
)

def send_slack_message(wekbook_url, data):

    response = requests.post(
        wekbook_url,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))

def set_and_log_config(config):

    config_str = json.dumps(config, indent=2)

    slack_message_payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{config_str}```"
                }
            }
        ]
    }

    send_slack_message(config['slack_webhook_url'], slack_message_payload)

    print(config_str)

    return config
