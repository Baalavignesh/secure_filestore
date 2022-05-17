# Secure FileStore

Secure drive to store files, track the version updates and download them

## Installation

FASTAPI is required to run the program locally and upload files to S3

```bash
pip install "uvicorn[standard]"

uvicorn main:app --reload;
```

## Usage

There are 3 main services used in application AuthHandler, FileHandler and DBHandler. Once the user is Authenticated a **JWT** is returned with the UserID and Email Address. These two variables are used to fetch and store data in **RDS and S3 Bucket**

## Handlers

**AuthHandler** will process the username, password and hashing methods. 

**DBHandler** is used set the configuration of the **MYSQL** and to send the data to RDS with the corresponding queries.

 **FileHandler** takes care of uploading the file to S3, fetching all files, versionID and generating the SignedURL for the files in Bucket.
