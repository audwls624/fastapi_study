from datetime import datetime
from dataclasses import asdict

import uvicorn
from fastapi import APIRouter, Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.common.config import conf
from app.database.connections import db, Base
from app.database.schema import User
from app.routes import index


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

    # router 정의
    app.include_router(index.router)
    return app


# app = create_app()
c = conf()
conf_dict = asdict(c)
app = FastAPI()
db.init_app(app, **conf_dict)

app.include_router(index.router)


if __name__ == "__main__":
    # uvicorn.run("main:app", host="0,0,0,0", port=8000, reload=conf().PROJ_RELOAD)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

