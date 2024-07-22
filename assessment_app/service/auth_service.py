from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(request: Request) -> str:
    """
    Get jwt_token from request cookies from database and return corresponding user id which is `email_id` to keep it simple.
    Verify the jwt_token is authentic (from database) and is not expired.
    """
    pass
