from fastapi import APIRouter, HTTPException
from models.signup import SignUp
from dbsetup import DBHandler
from routes.auth.auth import AuthHandler

user_signup = APIRouter()
auth_handler = AuthHandler()
db_handler = DBHandler()

# Signup Page


@user_signup.post('/signup', tags=["Authentication"])
async def signup(data: SignUp):
    hashed = auth_handler.hash_password(data.password)
    rows = db_handler.check_user(data.email)

    # New User
    if len(rows) == 0:
        curr_userId = db_handler.add_user(data, hashed)
        # Generate JWT and return for the user
        encoded_jwt = auth_handler.encode_jwt(
            {"Userid": curr_userId, "Email": data.email})

        return {'token': encoded_jwt}

    # User Already Present
    else:
        raise HTTPException(
            status_code=500, detail="User Already Exists/ Server Error"
        )
