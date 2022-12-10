from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    size: Optional[int] = Field(Query(default=50, alias="page[size]", ge=1, le=9999))
    number: Optional[int] = Field(Query(default=1, alias="page[number]", ge=1))

    class Config:
        allow_population_by_field_name = True
