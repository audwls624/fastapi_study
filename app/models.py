from enum import Enum
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserRegister(BaseModel):
    email: EmailStr = None
    password: str = None


class SnsType(str, Enum):
    email: str = 'Email'
    facebook: str = 'Facebook'
    google: str = 'Google'
    kakao: str = 'Kakao'


class Token(BaseModel):
    Authorization: str = None


class UserToken(BaseModel):
    id: int
    pw: str = None
    email: str = None
    name: str = None
    phone_number: str = None
    profile_image: str = None
    sns_type: str = None

    class Config:
        orm_mode = True
