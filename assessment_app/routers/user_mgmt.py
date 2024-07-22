from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from assessment_app.models.models import User, RegisterUserRequest

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(user: RegisterUserRequest) -> User:
    """
    Register a new user in database and save the login details (email_id and password) separately from User.
    Also, do necessary checks as per your knowledge.
    """
    pass


@router.post("/login", response_model=str)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    Login user after verification of credentials and add jwt_token in response cookies.
    Also, do necessary checks as per your knowledge.
    """

    jwt_token = None

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="jwt_token", value=f"Bearer {jwt_token}", httponly=True
    )
    return response
