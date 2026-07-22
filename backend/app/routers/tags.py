from backend.app.db_depends import get_session
from backend.app.models.tags import TagModel
from backend.app.schemas.tags import TagSchema
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/tags', tags=['tags'])


@router.get('/', response_model=list[TagSchema])
async def get_all_tags(
    session: Session = Depends(get_session),
) -> list[TagModel]:

    return list(session.scalars(select(TagModel)).all())


@router.get('/{tag_id}', response_model=TagSchema)
async def get_tag_by_id(
    tag_id: int, session: Session = Depends(get_session)
) -> TagModel:
    stmt = select(TagModel).where(TagModel.id == tag_id)
    tag = session.scalar(stmt)
    if not tag:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f'Тега с id: {tag_id} не найдено.',
        )
    return tag
