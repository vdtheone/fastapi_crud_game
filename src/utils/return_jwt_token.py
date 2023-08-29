import os
from fastapi import HTTPException, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session


SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def access_token_required(func):
    def inner(*args):
        try:
            request = None
            for i in args:
                if isinstance(i, Request):
                    request = i
                    break

            if request is None:
                raise HTTPException(status_code=500, detail="Request not found")

            access_token = request.headers.get("Authorization")
            token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            print(token)
            return func(*args)
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token Expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Provide valid Token")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return inner
