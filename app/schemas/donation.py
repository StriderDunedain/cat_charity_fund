from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class UserDonation(DonationBase):
    id: int
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class SuperUserDonation(UserDonation):
    user_id: Optional[int]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    close_date: Optional[datetime]
