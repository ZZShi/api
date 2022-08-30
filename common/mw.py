import time

from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Receive, Scope, Send, Message

from config import settings
from common.logger import log
from common.utils import random_str


class BaseMW:
    """基础 MiddleWare"""
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        req = Request(scope, receive, send)
        if not req.session.get("session"):
            req.session.setdefault("session", random_str())

        async def send_wrapper(message: Message) -> None:
            process_time = time.time() - start_time
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(process_time))
            await send(message)
        await self.app(scope, receive, send_wrapper)


class LogMW:
    """ 记录请求体和响应体"""
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http",):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        scope_path = scope['path']
        api_path = scope['path'].replace(settings.url_prefix, '')
        if (not scope_path.startswith(settings.url_prefix)) or (api_path in settings.logger_path_white_list):
            await self.app(scope, receive, send)
            return

        receive_ = await receive()

        async def receive():
            return receive_

        log.debug(f"{self.__class__.__name__} --> {scope['type']} > {scope['method']} > {scope['path']} ")
        log.debug(f"{self.__class__.__name__} --> request body: {receive_.get('body').decode()}")

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.body":
                log.debug(f"{self.__class__.__name__} --> response body: {message.get('body').decode()}")
            await send(message)

        await self.app(scope, receive, send_wrapper)
