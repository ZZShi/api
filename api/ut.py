from fastapi import APIRouter, Depends

from common.deps import Pager
from models.base import Event
from common.resp import RespSucc, RespPage
from schemas.event import EventCreate, EventUpdate, EventInfo, event_filter

app = APIRouter(prefix="/ut")


@app.get("/task", response_model=RespPage[EventInfo])
async def get_tasks(filters: dict = Depends(event_filter), pg: Pager = Depends(Pager())):
    queryset = Event.all()
    data = await pg.output(queryset, filters)
    return RespPage[EventInfo](data=data)


@app.post("/task", response_model=RespSucc[EventInfo])
async def create_task(info: EventCreate):
    data = await Event.create(**info.dict())
    return RespSucc(data=data)


@app.get("/task/{pk}", response_model=RespSucc[EventInfo])
async def get_task(pk: int):
    data = await Event.filter(id=pk).first()
    return RespSucc(data=data)


@app.patch("/task/{pk}", response_model=RespSucc[EventInfo])
async def get_task(pk: int, info: EventCreate):
    await Event.filter(id=pk).update(**info.dict())
    data = await Event.filter(id=pk)
    return RespSucc(data=data)


@app.delete("/task/{pk}", response_model=RespSucc[EventInfo])
async def get_task(pk: int):
    data = await Event.filter(id=pk).delete()
    return RespSucc(data=data)
