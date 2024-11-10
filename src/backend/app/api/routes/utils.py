from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.core.models.user import Message
from app.core.utils import generate_test_email, send_email

router = APIRouter()


@router.get("/health-check/")
async def health_check() -> bool:
    return True
