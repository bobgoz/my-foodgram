from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db_depends import get_session
from src.models.tags import TagModel
from src.schemas.tags import TagSchema

router = APIRouter(prefix='/tags', tags=['tags'])

@router.get('/', response_model=list[TagSchema])
async def get_all_tags(session: Session = Depends(get_session)):
    stmt = select(TagModel)
    return session.scalars(stmt).all()
