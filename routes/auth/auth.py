from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security, HTTPException
import os
import jwt
import bcrypt

class AuthHandler():
    SECRET_KEY = os.getenv('SECRET_KEY')
    security = HTTPBearer()

    def hash_password(self, password):
        # Converting String to Byte to Hash the password
        salt = bcrypt.gensalt()
        bytePass = bytes(password, 'utf-8')
        return bcrypt.hashpw(bytePass, salt)
        

    def encode_jwt(self, data):
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    def decode_jwt(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Signature has Expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid Token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_jwt(auth.credentials)
