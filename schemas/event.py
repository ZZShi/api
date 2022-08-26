from fastapi import Query
from pydantic import BaseModel

from common.resp import ORMModel


class EventUpdate(BaseModel):
    name: str


class EventCreate(EventUpdate):
    age: int


class EventInfo(ORMModel):
    name: str
    age: int


def event_filter(name: str = Query(None), age: str = Query(None)):
    query = {}
    if name:
        query.setdefault("name__icontains", name)
    if age:
        query.setdefault("age", age)
    return query
