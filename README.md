# Secure FileStore

Secure drive to store files, track the version updates and download them. 

## About the Project
Two layer encryption is used to store the user files with high security. 

The user is first authenticated with a Email and Password. Then the user selects a file to upload in S3 Bucket. The user is prompted for a password for each file. The file is encrypted with **Fernet** and the key generated is stored in a separate table along with file name and UserID in **Relational Database(RDS)**. Then the encrypted file is stored to S3 with Encryption enabled in the **AWS Bucket**. To download the file the password is verified and the object stream is fetched and decoded with the corresponding **Fernet Key** and sent to the user. 

**MYSQL** is used to store and query the data from table in **RDS**. All the password are hashed using **bcrypt** before storing it to the Database. 

## Built With
- FastAPI
- AWS Relational Database
- AWS S3


## Installation

1. Clone the Repository
```bash
https://github.com/Baalavignesh/secure_filestore
```

2. Install fastapi and other required dependancies

3. Create a .env file in the project root with the content listed below
```bash
SECRET_KEY=<Replace with your secret>

DB_ENDPOINT=<Replace with your RDS endpoint>
DB_USERNAME=<Replace with your RDS database username(MYSQL)>
DB_PASSWORD=<Replace with your RDS database username(MYSQL)>
DB_NAME=<Replace with your RDS database name(MYSQL)>

S3_BUCKET_NAME=<Replace with your S3 bucket name>
```

4. Run the application
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


## License
[MIT](https://choosealicense.com/licenses/mit/)
