from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.requests import Request

from app.database.connections import db
from app.database.schema import User

router = APIRouter()


@router.get("/")
async def index(session: Session = Depends(db.session)):
    """
    ELB 상태 체크용 API
    :param session:
    :return:
    """
    current_time = datetime.utcnow()
    return Response(f"TEST API (UTC: {current_time.strftime('%Y-%m-%dT%H:%M:%S')})")


@router.get("/test")
async def test(request: Request):
    """
    ELB 상태 체크용 API
    :param request:
    :return:
    """
    print("state.user: ", request.state.user)
    current_time = datetime.utcnow()
    return Response(f"TEST API (UTC: {current_time.strftime('%Y-%m-%dT%H:%M:%S')})")
