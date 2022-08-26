from fastapi import APIRouter, Depends
from tortoise.exceptions import DoesNotExist

from common.deps import Pager
from models.base import Events
from common.resp import RespSucc, RespPage
from schemas.event import EventCreate, EventUpdate, EventInfo, event_filter

app = APIRouter(prefix="/ut")


@app.get("/event", response_model=RespPage[EventInfo])
async def get_events(filters: dict = Depends(event_filter), pg: Pager = Depends(Pager)):
    queryset = Events.all()
    data = await pg.output(queryset, filters)
    return RespPage[EventInfo](data=data)


@app.post("/event", response_model=RespSucc[EventInfo])
async def create_event(info: EventCreate):
    data = await Events.create(**info.dict())
    return RespSucc(data=data)


@app.get("/event/{pk}", response_model=RespSucc[EventInfo])
async def get_event(pk: int):
    data = await Events.filter(id=pk).first()
    return RespSucc(data=data)


@app.patch("/event/{pk}", response_model=RespSucc[EventInfo])
async def get_event(pk: int, info: EventUpdate):
    if pk:
        raise DoesNotExist()
    await Events.filter(id=pk).update(**info.dict())
    data = await Events.filter(id=pk).first()
    return RespSucc(data=data)


@app.delete("/event/{pk}", response_model=RespSucc)
async def get_event(pk: int):
    data = await Events.filter(id=pk).delete()
    return RespSucc(data=data)
