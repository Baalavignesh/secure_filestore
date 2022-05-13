from distutils.command.upload import upload
from operator import imod
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from routes.auth.login import user_login
from routes.auth.signup import user_signup
from routes.file.upload import upload_file
from routes.file.getall import getall_files
from routes.file.getversion import getall_version
from routes.file.download import download_file

# Load the ENV File
load_dotenv()

# Initialize the FastAPI
app = FastAPI(title="SecureFileStore")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_login)
app.include_router(user_signup)
app.include_router(upload_file)
app.include_router(getall_files)
app.include_router(getall_version)
app.include_router(download_file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)