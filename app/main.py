from datetime import datetime
from dataclasses import asdict

import uvicorn
from fastapi import APIRouter, Depends
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.common.config import conf
from app.database.connections import db, Base
from app.database.schema import User
from app.routes import index, auth, users
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from app.middlewares.token_validator import access_control


def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    # 데이터 베이스 initialize

    # Redis intialize

    # middleware 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])
    # router 정의
    app.include_router(index.router)
    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    return app


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

# app = create_app()
c = conf()
conf_dict = asdict(c)
app = FastAPI()
db.init_app(app, **conf_dict)

# 미들웨어 정의(밑에 정의된 middleware 부터 실행 시작)
app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
app.add_middleware(
    CORSMiddleware,
    allow_origins=conf().ALLOW_SITE,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])

# router 정의
app.include_router(index.router)
app.include_router(auth.router, tags=["Authentication"], prefix="/api")
app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])


if __name__ == "__main__":
    # uvicorn.run("main:app", host="0,0,0,0", port=8000, reload=conf().PROJ_RELOAD)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

