import uuid
from sqlmodel import Session, select
from app.core.models.action import Action, ActionCreate


def create_action(*, session: Session, item_in: ActionCreate, owner_id: uuid.UUID) -> Action:
    db_item = Action.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_user_actions(session: Session, user_id: str, skip: int = 0, limit: int = 10):
    statement = select(Action).where(Action.owner_id == user_id).offset(skip).limit(limit)
    actions = session.exec(statement).all()
    return actions