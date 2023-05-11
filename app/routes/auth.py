import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.connections import db
from app.database.schema import User
from app.models import SnsType, Token, UserToken, UserRegister
from app.utils.common_utils import create_access_token, is_email_exist

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
    if sns_type != SnsType.email:
        result.update(msg="Invalid SNS Type")
        return JSONResponse(status_code=400, content=result)

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
    access_token = create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'password', 'marketing_agree'}), )
    result.update(
        Authorization=f"Bearer {access_token}"
    )
    return result


@router.post("/login/{sns_type}", status_code=200, response_model=Token)
async def login(sns_type: SnsType, user_info: UserRegister):
    result = dict()

    if sns_type != SnsType.email:
        result.update(msg="NOT_SUPPORTED")
        return JSONResponse(status_code=400, content=result)

    is_exist = await is_email_exist(user_info.email)
    if not user_info.email or not user_info.password:
        result.update(msg="Email and Password must be provided'")
        return JSONResponse(status_code=400, content=result)

    if not is_exist:
        result.update(msg="NO_MATCH_USER")
        return JSONResponse(status_code=400, content=result)

    user = User.get(email=user_info.email)
    is_verified = bcrypt.checkpw(user_info.password.encode("utf-8"), user.pw.encode("utf-8"))
    if not is_verified:
        return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))

    access_token = create_access_token(data=UserToken.from_orm(user).dict(exclude={'password', 'marketing_agree'}), )
    result.update(
        Authorization=f"Bearer {access_token}"
    )
    return result

