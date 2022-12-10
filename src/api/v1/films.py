from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination.bases import AbstractPage
from pydantic import BaseModel, Field

from core.config import Messages
from models.paginate import Pagination
from services.film import FilmService, get_film_service

router = APIRouter()
msg = Messages()


class FilmList(BaseModel):
    """Валидатор записи индекса 'movies' для списка."""

    id: str
    title: str
    imdb_rating: float


class FilmDetails(BaseModel):
    """Валидатор записи индекса 'movies' для объекта."""

    id: str
    title: str
    imdb_rating: float
    description: str
    genre: list
    actors_names: list
    writers_names: list


class FilterFilms(BaseModel):
    title: Optional[str] = Field(Query(default=None, alias="filter[title]"))
    imdb_rating: Optional[float] = Field(
        Query(default=None, alias="filter[imbd_rating]")
    )
    genre: Optional[str] = Field(Query(default=None, alias="filter[genre]"))
    actors_names: Optional[str] = Field(
        Query(default=None, alias="filter[actors_names]")
    )
    writers_names: Optional[str] = Field(
        Query(default=None, alias="filter[writers_names]")
    )

    class Config:
        allow_population_by_field_name = True


@router.get(
    "",
    response_model=List[FilmList],
    summary="Поиск кинопроизведений",
    description="Поиск по кинопроизведениям с возможностью импользования фильтров",
    response_description="Название, рейтинг, жанры, актёры и создатели фильма",
)
async def films(
    paginate: Pagination = Depends(),
    filters: FilterFilms = Depends(),
    sort: str = "-imdb_rating",
    service: FilmService = Depends(get_film_service),
) -> AbstractPage[FilmList]:
    """Получение списка фильмов.
    Args:
        filters: Параметры для фильтрации данных.
        sort: Параметр сортировки.
        service: Для получение данных.
    Returns:
        Страница списка фильмов.
    """
    obj_list = await service.get_obj_list(filters=filters, paginate=paginate, sort=sort)

    return list(obj_list)


@router.get(
    "/search",
    response_model=List[FilmList],
    summary="Полнотекстовый поиск",
    description="Осуществляет полнотекстовый поиск по всем полям",
    response_description="Название, рейтинг, жанры, актёры и создатели фильма",
)
async def films_search(
    paginate: Pagination = Depends(),
    query: str = "",
    service: FilmService = Depends(get_film_service),
) -> AbstractPage[FilmList]:
    """Получение списка фильмов.
    Args:
        query: Параметры строки запроса.
        service: Для получение данных.
        sort: Параметр сортировки.
    Returns:
        Страница списка фильмов.
    """
    obj_list = await service.get_obj_list(filters=query, paginate=paginate)

    return list(obj_list)


@router.get(
    "/{film_id}",
    response_model=FilmDetails,
    summary="Поиск по конкретному фильму",
    description="Осуществляет поиск по одному фильму",
    response_description="Название и  рейтинг фильма",
)
async def film_details(
    film_id: str, service: FilmService = Depends(get_film_service),
) -> FilmDetails:
    """Получение объекта фильма по id.
    Args:
        film_id: Id персоны.
        service: Сервис для получения данных.
    Returns:
        Объект фильма.
    """
    obj = await service.get_obj(film_id)
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=msg.FILM_NOT_FOUND)

    return obj
