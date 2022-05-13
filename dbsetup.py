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

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

    def createCursor(self):
        mycursor = self.mydb.cursor(buffered=True)
        return mycursor
