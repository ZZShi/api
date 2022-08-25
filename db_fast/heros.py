from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel


class HerosCreate(BaseModel):
    name: str
    secret_name: str
    age: Optional[int] = None


class HerosUpdate(BaseModel):
    name: str


class Heros(HerosCreate, SQLModel, table=True):
    ...


def heros_filters(name: Optional[str] = None):
    queryset = {}
    if name:
        # queryset.setdefault("name__icontains", name)
        queryset.setdefault("name", name)
    return queryset
