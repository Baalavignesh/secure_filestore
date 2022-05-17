from fastapi import APIRouter, Depends, HTTPException

from routes.auth.auth import AuthHandler
from routes.file.file_handle import FileHandler

auth_handler = AuthHandler()
file_handler = FileHandler()
getall_files = APIRouter()


@getall_files.post('/getall', tags=['File Management'])
async def getFiles(token=Depends(auth_handler.auth_wrapper)):
    try:
        userid = token['Email']
        print(userid)
        res = file_handler.get_files(userid)
        return res
    except Exception as e:
        HTTPException(status_code=404, detail=e)
