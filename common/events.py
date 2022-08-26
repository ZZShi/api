from typing import Callable

from aioredis import Redis
from fastapi import FastAPI

from common.logger import log
from db.redis import cache, cache_code
from db.mysql import register_mysql, close_connection


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """
    async def app_start() -> None:
        # APP启动完成后触发
        log.info("启动 FastApi")
        # 注册数据库
        await register_mysql(app)
        # # 注入缓存到app state
        app.state.cache = await cache()
        app.state.cache_code = await cache_code()
    return app_start


def shutdown(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """
    async def app_stop() -> None:
        # APP停止时触发
        log.info("停止 FastApi")
        # 断开数据库
        await close_connection()
        # 断开 Redis
        await app.state.cache.close()
        await app.state.cache_code.close()
        # cache: Redis = await app.state.cache
        # code: Redis = await app.state.cache_code
        # await cache.close()
        # await code.close()
    return app_stop
