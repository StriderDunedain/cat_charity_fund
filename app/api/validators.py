from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяем, нет ли проекта с таким же именем."""
    project_id = await charity_project_crud.get_id_by_name(charity_project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Благотворительный проект с таким именем уже существует!',
        )
    return


async def check_charity_project_exists(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    """Проверяем, существует ли проект."""
    charity_project = charity_project_crud.get(
        charity_project, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такого проекта нет!',
        )
    return


def check_charity_project_active(charity_project: CharityProject,) -> None:
    """Проверяем, заврешен ли проект."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя изменять уже завершенные проекты!'
        )
    return


def check_charity_project_full_amount(
    obj_in: CharityProject,
    charity_project: CharityProject,
) -> None:
    """Для умных."""
    if obj_in.full_amount < charity_project.invested_amount:
        raise HTTPException(
            detail='Нельзя менять сумму проекта в меньшую сторону',
            status_code=HTTPStatus.BAD_REQUEST,
        )
    return


async def check_none_fields_and_name(
    project: CharityProject,
    session: AsyncSession,
) -> None:
    if project.description == '' or project.name == '':
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя назначать такие пустые поля!',
        )
    await check_name_duplicate(project.name, session)
    return


def check_charity_project_has_money(
    charity_project: CharityProject
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалять проекты, в которые уже были вложены $!',
        )
    return
