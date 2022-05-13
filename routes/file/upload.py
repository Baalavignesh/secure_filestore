from fastapi import APIRouter, Depends, UploadFile, HTTPException
import tempfile
from ..auth.auth import AuthHandler
from .file_handle import FileHandler

auth_handler = AuthHandler()
file_handler = FileHandler()
upload_file = APIRouter()


@upload_file.post('/uploadfile', tags=['File Management'])
async def uploadFile(file: UploadFile, token=Depends(auth_handler.auth_wrapper)):
    try:
        print(token)
        with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as f:
            content = file.file.read()
            f.write(content)

            file_handler.file_upload(f.name, file.filename, token['userid'])
            return {"filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
