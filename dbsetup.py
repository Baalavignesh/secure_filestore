import mysql.connector
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class DBHandler():
    try:
        mydb = mysql.connector.connect(
            host=os.getenv('DB_ENDPOINT'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        mycursor = mydb.cursor(buffered=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    def check_user(self, email):
        # Check if user already exists
        sql = f"SELECT Email from Users where Email ='{email}'"
        self.mycursor.execute(sql)
        rows = self.mycursor.fetchall()
        return rows

    def add_user(self, data, hashed):
        # New User - Create DB
        sql = "INSERT INTO Users (Email, Username, Password) VALUES (%s, %s, %s)"
        val = (data.email, data.username, hashed)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        sql = f"SELECT Userid from Users where Email='{data.email}'"
        self.mycursor.execute(sql)
        U_ID = self.mycursor.fetchall()
        return U_ID

    def get_password(self, email):
        # Get Password for the given email id
        sql = f"SELECT Password, Userid from Users where Email ='{email}'"
        self.mycursor.execute(sql)
        fetched_user = self.mycursor.fetchall()
        return fetched_user

    def add_file(self, fileName, filePassword, fileKey, UserID):
        # Add the file to DB
        sql = "INSERT INTO Files (FileName, FilePassword, FileKey, Userid) VALUES (%s, %s, %s, %s)"
        val = (fileName, filePassword, fileKey, UserID)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def fetch_key(self, fileName, UserID):
        sql = f"SELECT FileKey from Files WHERE fileName='{fileName}' and Userid='{UserID}'"
        self.mycursor.execute(sql)
        fetched_key = self.mycursor.fetchall()
        return fetched_key

    def delete_file(self, fileName, UserID):
        sql = f"DELETE from Files WHERE FileName='{fileName}' AND Userid='{UserID}'"
        self.mycursor.execute(sql)
        self.db.commit()
