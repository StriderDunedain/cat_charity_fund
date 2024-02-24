from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import Donation, User


class DonationCRUD(CRUDBase):

    async def get_donation_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> list[Donation]:
        donation_id = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donation_id.scalars().first()


donation_crud = DonationCRUD(Donation)
