import os
from jose import ExpiredSignatureError, JWTError, jwt
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

def return_access_token(token):
    try:
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return token
    except ExpiredSignatureError as e:
        return "Token Expired"
    except JWTError: 
        return "Provide valid Token"
    except:
        return "Error"
   
