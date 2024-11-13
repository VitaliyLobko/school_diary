from sqlalchemy.orm import Session
from src.database.models import Group
from src.schemas import GroupModel


async def create_group(body: GroupModel, db: Session):
    group = (Group(**body.model_dump()))
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


async def get_groups(limit, offset, db: Session):
    groups = db.query(Group).order_by(Group.name).limit(limit).offset(offset).all()
    return groups
