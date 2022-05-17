from tokenize import String
from xmlrpc.client import boolean
from fastapi import APIRouter, Depends, UploadFile, HTTPException
import tempfile

from dbsetup import DBHandler
from ..auth.auth import AuthHandler
from .file_handle import FileHandler
from cryptography.fernet import Fernet


auth_handler = AuthHandler()
file_handler = FileHandler()
db_handler = DBHandler()
upload_file = APIRouter()


@upload_file.post('/uploadfile', tags=['File Management'])
async def uploadFile(file: UploadFile, filePass: str, filename: str, newVersion: bool,  token=Depends(auth_handler.auth_wrapper)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as f:
            # Get Content
            content = file.file.read()

            if(newVersion):
                # Fetch the Fernet Key to encrypt the new version file
                response = db_handler.fetch_key(filename, token['Userid'])
                fileKey = response[0]
                fileKey = bytes(fileKey[0], 'utf-8')

            else:
                # Encrypt the FilePassword
                hashedFilePass = auth_handler.hash_password(filePass)

                # Generate a File Key
                fileKey = Fernet.generate_key()

            fernet = Fernet(fileKey)
            encrypted = fernet.encrypt(content)
            f.write(encrypted)

            # First Upload to S3 then push to RDS - f.name is the location of the temporary created file
            file_handler.file_upload(f.name, filename, token['Email'])

            # Add data only if it is a new file for already existing file we just need to update the version
            if(newVersion == False):
                # Add the file name and secret to RDS
                db_handler.add_file(filename, hashedFilePass,
                                    fileKey, token['Userid'])

            return {"filename": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
