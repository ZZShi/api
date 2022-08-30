from typing import Union

from aioredis import Redis
from simpel_captcha import img_captcha
from fastapi import APIRouter, Depends, Request
from starlette.responses import StreamingResponse

from common.logger import log
from config import settings
from db.redis import get_captcha_code, get_redis
from models.user import User
from common.resp import RespSingle, RespFail
from schemas.user import UserRegister, UserInfo

app = APIRouter(prefix="/user")


@app.get("/captcha", summary='图片验证码')
async def image_captcha(req: Request, redis: Redis = Depends(get_redis)):
    image, text = img_captcha(byte_stream=True)
    log.info(f"验证码：{text}")
    session_value = req.session.get(settings.session_cookie_name)
    key = settings.captcha_key.format(session_value)
    await redis.setex(key, settings.captcha_seconds, text.lower())
    return StreamingResponse(content=image, media_type='image/jpeg')


@app.post('', response_model=Union[RespSingle[UserInfo], RespFail], summary='用户注册')
async def register(post: UserRegister, code_in_redis: str = Depends(get_captcha_code)):
    if code_in_redis is None:
        return RespFail(code=10302, msg='验证码已过期')
    if post.code.lower() != code_in_redis:
        return RespFail(code=10303, msg='验证码错误')

    if await User.filter(username=post.username).exists():
        return RespFail(code=10101, msg='当前用户名已被占用')
    user = await User.create(**post.dict())
    await user.set_password(post.password)
    user_info = UserInfo.from_orm(user)
    return RespSingle[UserInfo](data=user_info)
