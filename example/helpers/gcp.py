
import helpers
from helpers import *

def get_secrets(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_path(project_id, secret_id)
    resource_name = f"{parent}/versions/latest"
    response = client.access_secret_version(request={"name": resource_name})
    return response.payload.data.decode('UTF-8')

def create_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    response = client.create_secret(
        request={
            "parent": f"projects/{project_id}",
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}}
        }
    )

    return response

def create_secret_version(project_id, secret_id, secret_string):
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_path(project_id, secret_id)

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = secret_string.encode("UTF-8")

    # Add the secret version.
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )

    return response


def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    return buckets


def create_bucket(bucket_name):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name, location="europe-west2")

    print(
        "Created bucket {} in {} with storage class {}".format(
            bucket.name, bucket.location, bucket.storage_class
        )
    )
    return bucket


def upload_blob(bucket_name, data, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # data = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    print(f"Data uploaded to file {destination_blob_name}.")