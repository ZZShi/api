from fastapi import APIRouter


from .ut import app as ut
from .demo import app as demo
from .user import app as user
from .common import app as common


v1 = APIRouter(prefix="/api/v1")

v1.include_router(ut, tags=["自动化测试"])
v1.include_router(demo, tags=["示例"])
v1.include_router(user, tags=["用户中心"])
v1.include_router(common, tags=["通用"])
