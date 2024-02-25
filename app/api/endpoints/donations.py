from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationBase, SuperUserDonation, UserDonation
from app.services.investing import donating_logic

donation_router = APIRouter()


@donation_router.get(
    '/my',
    response_model=list[UserDonation],
    response_model_exclude_none=True,
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Какие пожертвования сделал определенный пользователь."""
    return [await donation_crud.get_donation_by_user(user, session)]


@donation_router.get(
    '/',
    response_model=list[SuperUserDonation],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Какие пожертвования были сделаны вообще?"""
    return await donation_crud.get_multi(session)


@donation_router.post(
    '/',
    response_model=UserDonation,
    response_model_exclude_none=True,
)
async def create_a_donation(
    donation: DonationBase,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.create(donation, session, user)
    donation = await donating_logic(donation, CharityProject, session)

    return donation
