from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination.bases import AbstractPage
from pydantic import BaseModel, Field

from core.config import Messages
from models.genre import GenreDetails, GenreList
from models.paginate import Pagination
from services.genre import GenreService, get_genre_service

router = APIRouter()
msg = Messages()


class FilterGenres(BaseModel):
    name: Optional[str] = Field(Query(default=None, alias="filter[name]"))

    class Config:
        allow_population_by_field_name = True


@router.get(
    "",
    response_model=List[GenreList],
    summary="Поиск по жанрам",
    description="Поиск по жанрам с возможностью импользования фильтров",
    response_description="Id жанра, название жанра",
)
async def genres(
    paginate: Pagination = Depends(),
    filters: FilterGenres = Depends(),
    service: GenreService = Depends(get_genre_service),
) -> AbstractPage[GenreList]:
    """Получение списка жанров.
    Args:
        filters: Параметры для фильтрации данных.
        _service: Для получение данных.
        sort: Параметр сортировки.
    Returns:
        Страница списка жанров.
    """
    obj_list = await service.get_obj_list(filters=filters, paginate=paginate)

    return list(obj_list)


@router.get(
    "/{genre_id}",
    response_model=GenreDetails,
    summary="Выбор жанра",
    description="Выбор одного жанра по id",
    response_description="Id жанра, название жанра и фильмы, относящиеся к этому жанру",
)
async def genre_details(
    genre_id: str, service: GenreService = Depends(get_genre_service)
) -> GenreDetails:
    """Получение объекта жанра по id.
    Args:
        genre_id: Id жанра.
        service: Сервис для получения данных.
    Returns:
        Объект жанра.
    """
    obj = await service.get_obj(genre_id)
    if not obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=msg.GENRE_NOT_FOUND
        )

    return obj
