from distutils.command.upload import upload
from fastapi import APIRouter, Depends, UploadFile, HTTPException
import tempfile

from requests import post
from ..auth.auth import AuthHandler
from .file_handle import FileHandler
import os

auth_handler = AuthHandler()
file_handler = FileHandler()
download_file = APIRouter()


# To download File Locally

# @download_file.post('/downloadfile', tags=['File Management'])
# def downloadFile(filename, token=Depends(auth_handler.auth_wrapper)):
#     try:
#         print(filename)
#         file_handler.download_file(filename)
#         return True
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=404, detail=e)


@download_file.post('/downloadfile', tags=['File Management'])
def downloadFile(filename, token=Depends(auth_handler.auth_wrapper)):
    try:
        print(filename)
        signed_url = file_handler.download_file(filename)
        return signed_url
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
