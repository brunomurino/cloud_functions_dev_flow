
import helpers
from helpers import *
from helpers import (
    gcp,
    mailerlite,
)

def run(config):
    pass

def entrypoint(request):

    config = set_and_log_config({
        "gcp_project_id": storage.Client().project,
        "env": os.environ.get('ENV', 'dev'),
        "job_name": os.environ.get('JOB_NAME', 'missing_job_name'),
        "request_method": request.method,
        "request_args": request.args.to_dict(flat=False),
        "request_data": request.form.to_dict(flat=False),
        "slack_webhook_url": os.environ['SLACK_WEBHOOK_URL'],
    })

    run(config)

    message = "Hello World!"
    return message