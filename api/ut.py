from fastapi import APIRouter

from models.base import Event
from common.resp import RespSucc, RespPage
from schemas.event import CreateEvent

app = APIRouter(prefix="/ut")


@app.get("/task", response_model=RespSucc[CreateEvent])
async def get_tasks(name: str):
    data = await Event.filter(name=name).limit(3).offset(2)
    return RespPage[CreateEvent](data=data)


@app.post("/task", response_model=RespSucc[CreateEvent])
async def create_task(info: CreateEvent):
    data = await Event.create(**info.dict())
    return RespSucc(data=data)


@app.get("/task/{pk}")
async def get_task(pk: int):
    data = await Event.filter(id=pk).first()
    return RespSucc(data=data)


@app.patch("/task/{pk}")
async def get_task(pk: int, info: CreateEvent):
    await Event.filter(id=pk).update(**info.dict())
    data = await Event.filter(id=pk)
    return RespSucc(data=data)


@app.delete("/task/{pk}")
async def get_task(pk: int):
    data = await Event.filter(id=pk).delete()
    return RespSucc(data=data)
