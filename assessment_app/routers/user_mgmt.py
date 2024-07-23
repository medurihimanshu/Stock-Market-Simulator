from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
import redis
from assessment_app.models.models import User, RegisterUserRequest
import os
from assessment_app.models.constants import JWT_TOKEN, REDIS_HOST, REDIS_PORT, PASSWORD, EMAIL, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from passlib.context import CryptContext  # for password hashing
import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt

router = APIRouter()
redis_client = redis.Redis(host=os.environ.get(REDIS_HOST), port=os.environ.get(REDIS_PORT), db=0)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=User)
async def register_user(user: RegisterUserRequest) -> User:
    """
    Register a new user in database and save the login details (email_id and password) separately from User.
    Also, do necessary checks as per your knowledge.
    """
    # 1. Has user already registered
    email_exists = redis_client.exists(user.email)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    # 2. Hash password before storing
    hashed_password = pwd_context.hash(user.password)

    # 3. Save login details in Redis CACHE for faster response
    user_data = {EMAIL: user.email, PASSWORD: hashed_password}
    redis_client.hset(user.email, mapping=user_data)

    return user
    

@router.post("/login", response_model=str)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    Login user after verification of credentials and add jwt_token in response cookies.
    Also, do necessary checks as per your knowledge.
    """

    # 1. Fetch email from Redis using the username (assuming username and email are the same)
    email = form_data.username
    user_data = redis_client.hgetall(email)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username, kindly register first",
        )

    # 2. Verify password
    user_data_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in user_data.items()}
    is_valid_password = pwd_context.verify(form_data.password, user_data_dict.get(PASSWORD))
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    # 3. Generate JWT token (replace with your JWT library)
    # jwt_token = create_jwt_token()  # Replace with your logic
    jwt_token = create_access_token(user_data_dict)

    # 4. Set JWT token in response cookie
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="jwt_token", value=jwt_token, httponly=True)

    return response


def generate_random_salt():
    return secrets.token_bytes(16).hex()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})

    try:
        encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_token
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token",
        ) from e