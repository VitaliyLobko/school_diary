from sqlalchemy.orm import Session
from src.database.models import Group
from src.schemas.groups import GroupModel


async def create_group(body: GroupModel, db: Session):
    group = Group(**body.model_dump())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


async def get_all(db: Session):
    total_students = db.query(Group).count()
    return total_students


async def get_groups(limit, offset, db: Session):
    groups = db.query(Group).order_by(Group.name).limit(limit).offset(offset).all()
    return groups


async def update_group(body: GroupModel, group: int, db: Session):
    for name, value in body:
        setattr(group, name, value)
    db.commit()
    return group


async def delete_group(group, db: Session):
    db.delete(group)
    db.commit()
    return group
