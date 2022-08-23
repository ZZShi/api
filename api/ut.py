from fastapi import APIRouter

from models.base import Event
from core.resp import RespSucc
from schemas.event import CreateEvent

app = APIRouter(prefix="/ut")


@app.get("/task")
async def get_tasks(name: str):
    data = await Event.filter(name=name).limit(3).offset(2)
    return RespSucc(data=data)


@app.post("/task")
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
