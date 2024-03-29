import re
from typing import Optional

from pydantic import BaseModel, Field, validator


# -------------------------------  检验函数  ---------------------------------------------
from common.resp import ORMModel
from schemas.enums.model import UserGender
from schemas.role import RoleInfoForLoginResp


def check_username(username: str) -> str:
    if ' ' in username:
        raise ValueError('用户名不能包含空格')
    if not username.isalnum():
        raise ValueError('用户名只能由字母和数字组成')
    if re.match(r'^\d', username):
        raise ValueError('用户名不能以数字开头')
    return username


def check_password(password: str) -> str:
    if re.match(r'^\d+$', password):
        raise ValueError("不能使用纯数字的密码")
    return password


# -------------------------------  请求部分  ---------------------------------------------
class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description='用户名')
    password: str = Field(..., min_length=6, max_length=20, description='密码')
    code: str = Field(..., min_length=4, max_length=4, description='验证码')

    _check_username = validator("username", allow_reuse=True)(check_username)
    _check_password = validator("password", allow_reuse=True)(check_password)


class UserRegister(UserLogin):
    password2: str = Field(..., min_length=6, max_length=20, description='密码2')

    @validator('password2')
    def passwords_match(cls, value, values, ):
        if 'password' in values and value != values['password']:
            raise ValueError('两次输入的密码不匹配')
        return value


class ModifyPassword(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=20, description='旧密码')
    new_password: str = Field(..., min_length=6, max_length=20, description='新密码')
    new_password2: str = Field(..., min_length=6, max_length=20, description='新密码2')

    _check_password = validator("*", allow_reuse=True)(check_password)

    @validator('new_password2')
    def passwords_match(cls, value, values, ):
        if 'new_password' in values and value != values['new_password']:
            raise ValueError('两次输入的密码不匹配')
        return value


# ModifyInfo = pydantic_model_creator(User, name='ModifyInfo', include=('nickname', 'full_name', 'gender'))
# 自动生成的模型，不支持枚举
class ModifyInfo(BaseModel):
    nickname: str | None = None
    full_name: str | None = None
    gender: UserGender = UserGender.unknown

    @validator('*')
    def blank_strings(cls, v):
        return None if v == "" else v


# -------------------------------  响应部分  ---------------------------------------------

class Token(ORMModel):
    access_token: str = Field(..., alias='accessToken')
    token_type: str = Field(..., alias='tokenType')


class UserInfo(ORMModel):
    """ 用户信息 """
    id: int = Field(..., alias='userId', description='用户ID')
    username: str = Field(..., alias='username', description='用户名')
    # nickname: Optional[str]
    # email: Optional[EmailStr]
    full_name: Optional[str] = Field(None, alias='realName', description="真实姓名")
    # is_superuser: bool = Field(..., alias='isSuperuser')
    # is_active: bool = Field(..., alias='isActive')
    head_img: Optional[str] = Field(None, alias='avatar', description="头像")
    # gender: UserGender
    # remarks: Optional[str]
    # phone_number: Optional[str] = Field(None, alias='phoneNumber')
    # create_time: datetime = Field(None, alias='createTime')
    # update_time: datetime = Field(None, alias='updateTime')
    remarks: Optional[str] = Field(None, alias='desc', description="介绍")


class LoginResult(ORMModel):
    """ 响应登陆 """
    id: int = Field(..., gt=0, alias='userId', description='用户ID')
    token: str
    role: RoleInfoForLoginResp


class UserInfoToken(UserInfo):
    """ 用户信息 + Token"""
    token: Token
