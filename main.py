import uvicorn
from fastapi import FastAPI

from config import settings
from common.mw import LogMW
from common.events import startup, shutdown
from common.exception import register_exceptions
from api import ut, demo,common

app = FastAPI(
    debug=settings.APP_DEBUG
)

# 注册异常处理
app = register_exceptions(app)

# 注册中间件，洋葱模型
app.add_middleware(LogMW)

# 注册事件
app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", shutdown(app))


app.include_router(ut, prefix='/api/v1', tags=["自动化测试"])
app.include_router(common, prefix='/api/v1', tags=["接口调试"])
app.include_router(demo, prefix='/api/v1', tags=["Demo"])


if __name__ == '__main__':
    uvicorn.run(app="main:app")
