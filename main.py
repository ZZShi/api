import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config import settings
from common.mw import LogMW
from common.events import startup, shutdown
from common.exception import register_exceptions
from api import v1

app = FastAPI(
    debug=settings.debug,
    swagger_ui_oauth2_redirect_url=settings.swagger_ui_oauth2_redirect_url
)

# 注册异常处理
app = register_exceptions(app)

# 注册中间件，洋葱模型
app.add_middleware(LogMW)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key,
                   session_cookie=settings.session_cookie,
                   max_age=settings.session_max_age)

# 注册事件
app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", shutdown(app))


app.include_router(v1)


if __name__ == '__main__':
    uvicorn.run(app="main:app")
