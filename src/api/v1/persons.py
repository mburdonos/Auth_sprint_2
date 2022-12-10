from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination.bases import AbstractPage
from pydantic import BaseModel, Field

from core.config import Messages
from models.paginate import Pagination
from models.person import PersonDetails, PersonList
from services.person import PersonService, get_person_service

router = APIRouter()
msg = Messages()


class FilterPerson(BaseModel):
    full_name: Optional[str] = Field(Query(default=None, alias="filter[full_name]"))

    class Config:
        allow_population_by_field_name = True


@router.get(
    "",
    response_model=List[PersonList],
    summary="Поиск персон",
    description="Поиск по людям с возможностью импользования фильтров",
    response_description="Id человека, его полное имя",
)
async def persons(
    paginate: Pagination = Depends(),
    filters: FilterPerson = Depends(),
    service: PersonService = Depends(get_person_service),
) -> AbstractPage[PersonList]:
    """Получение списка персон.
    Args:
        filters: Параметры для фильтрации данных.
        service: Сервис для олучения данных.
    Returns:
        Страница списка песрон.
    """
    obj_list = await service.get_obj_list(filters=filters, paginate=paginate)

    return list(obj_list)


@router.get(
    "/search",
    response_model=List[PersonList],
    summary="Полнотекстовый поиск по персонам",
    description="Полнотекстовый поиск по людям",
    response_description="Id человека, его полное имя",
)
async def person_search(
    paginate: Pagination = Depends(),
    query: str = "",
    service: PersonService = Depends(get_person_service),
) -> AbstractPage[PersonList]:
    """Получение списка персон в поиске.
    Args:
        query: Параметры строки запроса.
        service: Сервис для получения данных.
    Returns:
        Страница списка песрон.
    """
    obj_list = await service.get_obj_list(filters=query, paginate=paginate)

    return list(obj_list)


@router.get(
    "/{person_id}",
    response_model=PersonDetails,
    summary="Выбрать конкретного человека",
    description="Выбирает конкретного человека по его id",
    response_description="Id человека, его полное имя, в каком статусе и в каких фильмах он снимался",
)
async def person_details(
    person_id: str, service: PersonService = Depends(get_person_service)
) -> PersonDetails:
    """Получение объекта персоны по id.
    Args:
        person_id: Id персоны.
        service: Сервис для получения данных.
    Returns:
        Объект персоны.
    """
    obj = await service.get_obj(person_id)
    if not obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=msg.PERSON_NOT_FOUND
        )

    return obj
