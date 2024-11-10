import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.core.models.action import Action, ActionCreate, ActionPublic, ActionsPublic, ActionUpdate
from app.core.models.user import Message

router = APIRouter()


@router.get("/", response_model=ActionsPublic)
def read_actions(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve actions.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Action)
        count = session.exec(count_statement).one()
        statement = select(Action).offset(skip).limit(limit)
        actions = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Action)
            .where(Action.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Action)
            .where(Action.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        actions = session.exec(statement).all()

    return ActionsPublic(data=actions, count=count)


@router.get("/{id}", response_model=ActionPublic)
def read_action(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get action by ID.
    """
    action = session.get(Action, id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if not current_user.is_superuser and (action.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return action


@router.post("/", response_model=ActionPublic)
def create_action(
    *, session: SessionDep, current_user: CurrentUser, action_in: ActionCreate
) -> Any:
    """
    Create new action.
    """
    action = Action.model_validate(action_in, update={"owner_id": current_user.id})
    session.add(action)
    session.commit()
    session.refresh(action)
    return action


@router.put("/{id}", response_model=ActionPublic)
def update_action(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    action_in: ActionUpdate,
) -> Any:
    """
    Update an action.
    """
    action = session.get(Action, id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if not current_user.is_superuser and (action.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = action_in.model_dump(exclude_unset=True)
    action.sqlmodel_update(update_dict)
    session.add(action)
    session.commit()
    session.refresh(action)
    return action


@router.delete("/{id}")
def delete_action(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an action.
    """
    action = session.get(Action, id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if not current_user.is_superuser and (action.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(action)
    session.commit()
    return Message(message="Action deleted successfully")
