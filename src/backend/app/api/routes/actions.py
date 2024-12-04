import uuid
from typing import Any, Optional


from fastapi import APIRouter, HTTPException, Form, Depends

from pydantic import BaseModel
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.core.models.action import Action, ActionCreate, ActionPublic, ActionsPublic, ActionUpdate
from app.core.models.user import Message

#from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)
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

# class ServiceCredentials(BaseModel):
#     username: str = Form(..., min_length=1, max_length=255)
#     password: str = Form(..., min_length=1, max_length=255)
# @router.post("/analyze-job-offers")
# async def scrap_page(
#     username: str = Form(..., min_length=1, max_length=255),
#     password: str = Form(..., min_length=1, max_length=255),
# ) -> Any:
#     """
#     Analyze job offers.
#     """
#     print(f"username: {username}")
#     logger.debug(f"username: {username}")
#
#     async def get_page_content(username, password):
#         async with async_playwright() as p:
#             # Launch the browser in headless mode (set headless=False to see the browser in action)
#             browser = await p.chromium.launch(headless=False)
#             try:
#                 context = await browser.new_context()
#                 page = await context.new_page()
#
#                 # Navigate to Upwork login page
#                 await page.goto('https://www.upwork.com/ab/account-security/login')
#
#                 # Step 1: Enter Username/Email and click "Continue"
#                 await page.fill('#login_username', username)
#                 await page.click('#login_password_continue')
#
#                 # Wait for the password input field to appear
#                 await page.wait_for_selector('#login_password', timeout=5000)
#
#                 # Step 2: Enter Password and click "Log in"
#                 await page.fill('#login_password', password)
#                 await page.click('#login_control_continue')
#
#                 # Wait for navigation or a specific element indicating login success
#                 await page.wait_for_navigation()
#
#                 # Print the content of the current page
#                 content = await page.content()
#                 print(content)
#                 return content
#             finally:
#                 # Ensure the browser is closed even if an error occurs
#                 await browser.close()
#
#     try:
#         content = await get_page_content(username, password)
#         return content
#     except Exception as e:
#         logger.error(f"Error during page scraping: {e}")
#         raise HTTPException(status_code=400, detail=f"An error occurred while scraping job offers.: {e}")


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
