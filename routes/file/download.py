import tempfile
from fastapi import APIRouter, Depends, HTTPException

from dbsetup import DBHandler
from ..auth.auth import AuthHandler
from .file_handle import FileHandler

auth_handler = AuthHandler()
file_handler = FileHandler()
download_file = APIRouter()
db_handler = DBHandler()

# To download File Locally
# @download_file.post('/downloadfile', tags=['File Management'])
# def downloadFile(filename, token=Depends(auth_handler.auth_wrapper)):
#     try:
#         file_handler.download_file(filename)
#         return True
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=e)

# To get {PerSignedUrl}
# @download_file.post('/downloadfile', tags=['File Management'])
# def downloadFile(filename, token=Depends(auth_handler.auth_wrapper)):
#     try:
#         signed_url = file_handler.generate_signedUrl(filename)
#         return signed_url
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=e)


# To get the object in form of bytes
@download_file.post('/downloadfile', tags=['File Management'])
def downloadFile(filename, versionID, token=Depends(auth_handler.auth_wrapper)):
    try:
        user_mail = token['Email']
        filename = user_mail+'/'+filename
        obj_res = file_handler.get_object(filename, versionID)
        body = obj_res.get()['Body'].read()
        
        fileKey = db_handler.fetch_key(filename, token['Userid'])
        
        
        with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as f:
            
            
            
            f.write(body)
        return obj_res
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
