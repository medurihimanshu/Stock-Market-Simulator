from errno import EMLINK
from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from assessment_app.models.constants import EMAIL, JWT_TOKEN, SECRET_KEY, ALGORITHM, REDIS_HOST, REDIS_PORT
from jose import JWTError, jwt
import redis
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
redis_client = redis.Redis(host=os.environ.get(REDIS_HOST), port=os.environ.get(REDIS_PORT), db=0)

def get_current_user(request: Request) -> str:
    """
    Get jwt_token from request cookies from database and return corresponding user id which is `email_id` to keep it simple.
    Verify the jwt_token is authentic (from database) and is not expired.
    """
    token = request.cookies.get(JWT_TOKEN)
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    print(f'Test Token - {token}')
    email = verify_jwt_token(token)
    print(f'Test Email - {email}')
    if email is None or not redis_client.exists(email):
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    return email

def verify_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f'Test Payload - {payload}')
        email: str = payload.get(EMAIL)
        if email is None:
            raise JWTError
        return email
    except JWTError:
        return None

