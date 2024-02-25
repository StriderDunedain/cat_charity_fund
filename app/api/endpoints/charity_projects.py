from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_active,
    check_charity_project_exists,
    check_charity_project_full_amount,
    check_charity_project_has_money,
    check_none_fields_and_name,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import donating_logic

charity_project_router = APIRouter()


@charity_project_router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Посмотреть все Благотворительные Проекты."""
    return await charity_project_crud.get_multi(session)


@charity_project_router.get(
    '/{project_id}',
    response_model=list[CharityProjectDB],
)
async def get_charity_projects(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Посмотреть Благотворительный Проект по id."""
    return await charity_project_crud.get(project_id, session)


@charity_project_router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание нового Благотворительного Проекта. Superuser-only."""
    await check_none_fields_and_name(charity_project, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    new_charity_project = await donating_logic(new_charity_project, Donation, session)

    return new_charity_project


@charity_project_router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project_by_id(
    project_id: int,
    project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Частичное обновление Благотворительного Проекта. Superuser-only."""
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    await check_charity_project_exists(project_id, session)
    check_charity_project_active(charity_project)
    await check_none_fields_and_name(project, session)

    if project.full_amount is None:
        charity_project = await charity_project_crud.update(
            charity_project, project, session
        )
        return charity_project

    check_charity_project_full_amount(project, charity_project)
    charity_project = await charity_project_crud.update(
        charity_project, project, session
    )
    charity_project = await donating_logic(charity_project, Donation, session)

    return charity_project


@charity_project_router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаление Благотворительного Проекта. Superuser-only."""
    await check_charity_project_exists(project_id, session)
    charity_project = await charity_project_crud.get(project_id, session)
    check_charity_project_active(charity_project)
    check_charity_project_has_money(charity_project)
    charity_project = await charity_project_crud.remove(charity_project, session)

    return charity_project
