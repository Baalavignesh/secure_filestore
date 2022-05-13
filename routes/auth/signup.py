from fastapi import APIRouter, HTTPException
from models.signup import SignUp
from dbsetup import DBHandler
from routes.auth.auth import AuthHandler

user_signup = APIRouter()
auth_handler = AuthHandler()

# Signup Page


@user_signup.post('/signup', tags=["Authentication"])
async def signup(data: SignUp):
    try:
        hashed = auth_handler.hash_password(data.password)

        # Check if user already exists
        sql = f"SELECT email from userinfo where email ='{data.email}'"

        db_handler = DBHandler()
        mycursor = db_handler.createCursor()
        mycursor.execute(sql)

        rows = mycursor.fetchall()

        if len(rows) == 0:
            # New User - Create DB
            sql = "INSERT INTO userinfo (email, username, password) VALUES (%s, %s, %s)"
            val = (data.email, data.username, hashed)
            mycursor.execute(sql, val)

        else:
            # User Already Present
            raise HTTPException(
                status_code=409, detail="User Already Exist"
            )

        db_handler.mydb.commit()

        # Generate JWT and return for the user
        encoded_jwt = auth_handler.encode_jwt({"userid": data.email})

        return {'token': encoded_jwt}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=e
        )
