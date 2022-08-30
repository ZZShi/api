from fastapi import APIRouter


from .ut import app as ut
from .test import app as test
from .user import app as user


v1 = APIRouter(prefix="/api/v1")

v1.include_router(ut, tags=["自动化测试"])
v1.include_router(test, tags=["接口测试"])
v1.include_router(user, tags=["用户中心"])
