from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist

from common.auth import create_access_token
from common.deps import Pager
from models.base import Events
from common.resp import RespSucc, RespPage, RespFail
from models.user import User
from schemas.event import EventCreate, EventUpdate, EventInfo, event_filter
from schemas.user import Token


app = APIRouter(prefix="/test")


@app.post('/token', summary='获取 token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if user is None:
        return RespFail(code=10201, msg='用户名与密码不匹配')
    if not user.check_password(form_data.password):
        return RespFail(code=10201, msg='用户名与密码不匹配')
    access_token = create_access_token(data={"sub": user.username})
    token_data = Token(access_token=access_token, token_type='bearer').dict(by_alias=False)
    return token_data


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
