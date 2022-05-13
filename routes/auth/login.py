# Login Page
from fastapi import APIRouter, HTTPException
from models.login import Login
from dbsetup import DBHandler
import bcrypt
from routes.auth.auth import AuthHandler

user_login = APIRouter()
auth_handler = AuthHandler()


@user_login.post("/login", tags=["Authentication"])
async def login(data: Login):
    # Check if user already exists
    sql = f"SELECT password from userinfo where email ='{data.email}'"
    db_handler = DBHandler()

    mycursor = db_handler.createCursor()

    mycursor.execute(sql)

    result = mycursor.fetchall()
    hashedPass = ''

    # User Found
    if result:
        print(result)
        userData = result[0]
        # Get the Password Hash for the entered email ID - Data is returned in form of tuple
        hashedPass = userData[0]

        # Convert the password from String to Bytes
        # Password Entered by the User
        bytePass = bytes(data.password, 'utf-8')
        byteHashedPass = bytes(hashedPass, 'utf-8')

        # Check the Hashed Password and Entered Password
        if bcrypt.checkpw(password=bytePass, hashed_password=byteHashedPass):
            encoded_jwt = auth_handler.encode_jwt({"userid": data.email})

            # Return JWT to the User - Store it locally
            return {"token": encoded_jwt}

        else:
            # Wrong Password
            raise HTTPException(
                status_code=401, detail="Wrong Password"
            )
    else:
        # No User Found
        raise HTTPException(
            status_code=404, detail="No User Found"
        )
