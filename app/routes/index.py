from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.database.connections import db
from app.database.schema import User

router = APIRouter()


@router.get("/")
async def index(session: Session = Depends(db.session)):
# async def index():
    """
    ELB 상태 체크용 API
    :param session:
    :return:
    """
    User.create(session, auto_commit=True)
    current_time = datetime.utcnow()
    return Response(f"TEST API (UTC: {current_time.strftime('%Y-%m-%dT%H:%M:%S')})")
