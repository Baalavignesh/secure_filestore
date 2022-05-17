from http import client
from fastapi import HTTPException
import boto3
import os

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


class FileHandler:

    bucket_name = os.getenv('S3_BUCKET_NAME')

    def file_upload(self, file, fileName, token):
        s3_resource.meta.client.upload_file(file, self.bucket_name,
                                            token+'/{}'.format(fileName))

    def get_files(self, username):
        response = s3_client.list_objects(
            Bucket=self.bucket_name, Prefix=username)
        return response

    def get_versions(self, filename):
        response = s3_client.list_object_versions(
            Bucket=self.bucket_name,
            Prefix=filename
        )
        return response

    def generate_signedUrl(self, filename, versionID):
        # Generate PreSigned Url
        response = s3_client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket_name, 'Key': filename, 'VersionId': versionID}, ExpiresIn=3600)
        return response

    def get_object(self, filename, versionID):
        # Get the File Object
        response = s3_client.get_object(
            Bucket=self.bucket_name, Key=filename, VersionId=versionID
        )
        return response

    def download_locally(self, filename):
        download_name = os.path.basename(filename)
        s3_resource.meta.client.download_file(
            Bucket=self.bucket_name, Key=filename, Filename=download_name)
        return True

    def delete_file():
        return False
