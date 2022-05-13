from http import client
from fastapi import HTTPException
import boto3
import os

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


class FileHandler:

    bucket_name = os.getenv('S3_BUCKET_NAME')

    def file_upload(self, file, fileName, token):
        s3_resource.upload_file(file, self.bucket_name,
                                token+'/{}'.format(fileName))

    def get_files(self, username):
        print('inside' + username)
        print('get file')
        response = s3_client.list_objects(
            Bucket=self.bucket_name, Prefix=username)
        print(response)
        return response

    def get_versions(self, filename):
        response = s3_client.list_object_versions(
            Bucket=self.bucket_name,
            Prefix=filename
        )
        return response

    def download_file(self, filename):
        try:
            print(filename)

            # Generate PreSigned Url
            response = s3_client.generate_presigned_url(
                'get_object', Params={'Bucket': self.bucket_name, 'Key': filename}, ExpiresIn=3600)
            print(response)
            return response
            # To download locally

            # download_name = os.path.basename(filename)
            # s3_resource.meta.client.download_file(
            #     Bucket=self.bucket_name, Key=filename, Filename=download_name)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail=e)

    def delete_file():
        return False
