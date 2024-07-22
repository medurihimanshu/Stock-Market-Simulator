from assessment_app.repository.database import Base


class UserCredentials(Base):
    email: str
    password_hash: str
    random_salt: str

    class Config:
        orm_mode = True
