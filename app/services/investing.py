from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def dryify(
    obj: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    """Making code dryer. Get it?"""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()

    return obj


async def money_money_money(
    obj_in: Union[CharityProject, Donation],
    other_model: Union[CharityProject, Donation],
) -> list[CharityProject, Donation]:
    """Go-go-go, ABBA!"""
    to_pay_obj_in = obj_in.full_amount - obj_in.invested_amount
    to_pay_model = other_model.full_amount - other_model.invested_amount

    if to_pay_obj_in > to_pay_model:
        obj_in.invested_amount += to_pay_model
        other_model = await dryify(other_model)
    if to_pay_obj_in == to_pay_model:
        obj_in = await dryify(obj_in)
        other_model = await dryify(other_model)
    else:
        other_model.invested_amount += to_pay_obj_in
        obj_in = await dryify(obj_in)

    return [obj_in, other_model]


async def donating_logic(
    obj_in: Union[CharityProject, Donation],
    other_model: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    """Some Math-big brain time."""
    models_to_iter_through = await session.execute(
        select(other_model).where(
            other_model.fully_invested == False  # noqa
        ).order_by(
            other_model.create_date
        )
    )
    for a_model in models_to_iter_through.scalars().all():
        obj_in, other_model = await money_money_money(
            obj_in, a_model
        )
        session.add(obj_in)
        session.add(other_model)
    await session.commit()
    await session.refresh(obj_in)

    return obj_in
