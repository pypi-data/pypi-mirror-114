from typing import Union
from pathlib import Path
import os

from google.oauth2 import service_account
from google.cloud import storage

from tqdm import tqdm

credentials = service_account.Credentials.from_service_account_file(os.environ['GCLOUD_CREDENTIALS'])
client = storage.Client(project=os.environ['GCLOUD_PROJECT'], credentials=credentials)


def set_gcp_creds(project_name: str, path_to_creds: Union[Path, str]) -> storage.Client:
    credentials = service_account.Credentials.from_service_account_file(path_to_creds)
    client = storage.Client(project=project_name, credentials=credentials)
    return client


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None, client=client):
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = client.list_blobs(
        bucket_name, prefix=prefix, delimiter=delimiter
    )

    return list(blobs)


def download_blob(blob, dst, client=client):
    with open(dst, 'wb') as file_obj:
        client.download_blob_to_file(blob, file_obj)


def download_gs_folder(bucket, gs_path, dst_path, client=client):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    blobs = list_blobs_with_prefix(bucket, gs_path, client=client)
    blobs = list(blobs)
    print('Download starting - will print "DONE" when finished!')
    for blob in tqdm(blobs):
        fname = Path(blob.name).name
        dst = os.path.join(dst_path, fname)
        print(f'Downloading: {fname}')
        print(f'To: {dst}')
        download_blob(blob, dst, client=client)
    print("DONE")


def rename_blob(blob: storage.blob.Blob, new_name, client=client):
    """Renames a blob."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # new_name = "new-object-name"

    bucket = client.bucket(blob.bucket.name)

    new_blob = bucket.rename_blob(blob, new_name)

    print(f"Blob {blob.name} has been renamed to {new_blob.name}")


def upload_blob(bucket_name, source_file_name, destination_blob_name, client=client):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {os.path.join(bucket_name, destination_blob_name)}."
    )
