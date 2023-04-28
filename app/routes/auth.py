import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import models
from app.common.constants import JWT_ALGORITHM, JWT_SECRET
from app.database.connections import db
from app.database.schema import User
from app.models import SnsType, Token, UserToken, UserRegister
from app.utils import create_access_token, is_email_exist


router = APIRouter(prefix="/auth")


@router.post("/register/{sns_type}", status_code=201, response_model=Token)
async def register(sns_type: SnsType, register_info: UserRegister, session: Session = Depends(db.session)):
    """
    회원가입 API
    :param sns_type:
    :param register_info:
    :param session:
    :return:
    """

    result = dict()
    if sns_type == SnsType.email:
        user_email = register_info.email
        user_password = register_info.password
        is_exists = await is_email_exist(user_email)

        if not user_email or not user_password:
            result.update(msg="Email and Password must be provided")
            return JSONResponse(status_code=400, content=result)

        if is_exists:
            result.update(msg="Email exists")
            return JSONResponse(status_code=400, content=result)

        hash_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        new_user = User.create(session, auto_commit=True, password=hash_password, email=user_email)
        token = dict(
            Authorizaion=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'password', 'phone_number', 'name', 'profile_image', 'email', 'marketing_agree'}),)}"
        )
        return token

    result.update(msg="Invalid SNS Type")
    return JSONResponse(status_code=400, content=result)

