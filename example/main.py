
import helpers
from helpers import *
from helpers import (
    gcp,
)

def entrypoint(request):

    config = {
        "gcp_project_id": storage.Client().project,
        "env": os.environ.get('ENV', 'dev'),
        "job_name": os.environ.get('JOB_NAME', 'missing_job_name'),
        "request_method": request.method,
        "request_args": request.args.to_dict(flat=False),
        "request_data": request.form.to_dict(flat=False),
        "slack_webhook_url": os.environ['SLACK_WEBHOOK_URL'],
    }

    log_config(config)

    list_of_buckets = gcp.list_buckets()
    buckets = [bucket.name for bucket in list_of_buckets]

    send_slack_message(config['slack_webhook_url'], {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"List of Buckets:\n```{buckets}```"
                }
            }
        ]
    })

    message = "Hello World!"
    return message