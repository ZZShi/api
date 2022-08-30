from typing import Union

from aioredis import Redis
from simpel_captcha import img_captcha
from fastapi import APIRouter, Depends, Request
from starlette.responses import StreamingResponse

from common.auth import create_access_token, get_current_active_user
from common.logger import log
from config import settings
from db.redis import get_captcha_code, get_redis
from models.user import User
from common.resp import RespSingle, RespFail, RespSucc
from schemas.role import RoleInfoForLoginResp
from schemas.user import UserRegister, UserInfo, UserLogin, LoginResult, ModifyPassword, ModifyInfo

app = APIRouter(prefix="/user")


@app.get("/captcha", summary='图片验证码')
async def image_captcha(req: Request, redis: Redis = Depends(get_redis)):
    image, text = img_captcha(byte_stream=True)
    log.info(f"验证码：{text}")
    session_value = req.session.get(settings.session_cookie_name)
    key = settings.captcha_key.format(session_value)
    await redis.setex(key, settings.captcha_seconds, text.lower())
    return StreamingResponse(content=image, media_type='image/jpeg')
    # return RespSucc(data={"text": text})


@app.post('/register', response_model=Union[RespSingle[UserInfo], RespFail], summary='用户注册')
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


@app.post('/token', response_model=Union[RespSingle[LoginResult], RespFail], summary='用户登录')
async def login(post: UserLogin, code_in_redis: str = Depends(get_captcha_code)):
    if code_in_redis is None:
        return RespFail(code=10302, msg='验证码已过期')
    if post.code.lower() != code_in_redis:
        return RespFail(code=10303, msg='验证码错误')

    user = await User.get_or_none(username=post.username)
    if not user:
        return RespFail(code=10301, msg="账户名或密码错误")
    if not user.check_password(post.password):
        return RespFail(code=10301, msg="账户名或密码错误")

    access_token = create_access_token(data={"sub": post.username})

    role_name = "超级管理员" if user.is_superuser else "普通管理员"
    role_value = "超级管理员" if user.is_superuser else "普通管理员"
    role_info = RoleInfoForLoginResp(role_name=role_name, value=role_value)

    login_info = LoginResult(id=user.id, token=access_token, role=role_info)
    return RespSingle[LoginResult](data=login_info)


@app.get('/me', response_model=Union[RespSingle[UserInfo], RespFail], summary='获取用户信息')
async def get_my_info(user: User = Depends(get_current_active_user)):
    user_info = UserInfo.from_orm(user)
    return RespSingle[UserInfo](data=user_info)


@app.put('/me', response_model=Union[RespSingle[UserInfo], RespFail], summary='修改用户信息')
async def change_my_info(info: ModifyInfo, user: User = Depends(get_current_active_user)):
    await user.update_from_dict(info.dict(exclude_unset=True, exclude_none=True))
    await user.save()
    user_info = UserInfo.from_orm(user)
    return RespSingle[UserInfo](data=user_info)


@app.put("/password", response_model=Union[RespSucc, RespFail], summary='修改密码')
async def change_pwd(pwd: ModifyPassword, user: User = Depends(get_current_active_user)):
    if not user.check_password(pwd.old_password):
        return RespFail(code=10401, msg="旧密码错误")
    await user.set_password(pwd.new_password)
    return RespSucc(msg="修改密码成功")
