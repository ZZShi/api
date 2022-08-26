from typing import Union

from aioredis.exceptions import ConnectionError as RedisConnectionError
from fastapi import HTTPException, Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from tortoise.exceptions import (DBConnectionError as MysqlConnectionError, DoesNotExist as MysqlDoesNotExist,
                                 IntegrityError as MysqlIntegrityError, OperationalError as MysqlOperationalError,
                                 ValidationError as MysqlValidationError)

from common.logger import log
from .resp import RespFail


async def redis_connection_error(_: Request, exc: RedisConnectionError):
    """     redis连接错误    """
    log.error(f"redis连接错误  {str(exc)}")
    return JSONResponse(RespFail(code=500, msg="Redis 连接错误").dict(by_alias=True),
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def mysql_connection_error(_: Request, exc: MysqlConnectionError):
    """     数据库连接错误    """
    log.error(f"数据库连接错误  {str(exc)}")
    return JSONResponse(RespFail(code=500, msg="数据库连接错误").dict(by_alias=True),
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def mysql_validation_error(_: Request, exc: MysqlValidationError):
    """     数据库字段验证错误    """
    log.error(f"数据库字段验证错误  {str(exc)}")
    return JSONResponse(RespFail(code=422, msg="数据库字段验证错误", data=str(exc)).dict(by_alias=True),
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def mysql_integrity_error(_: Request, exc: MysqlIntegrityError):
    """    数据库完整性错误    """
    log.error(f"数据库完整性错误  {exc}")
    return JSONResponse(RespFail(code=422, msg="数据库完整性错误", data=str(exc)).dict(by_alias=True),
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def mysql_does_not_exist(_: Request, exc: MysqlDoesNotExist):
    """     mysql 查询对象不存在异常处理    """
    log.error(f"数据库查询对象不存在异常 {str(exc)}")
    return JSONResponse(RespFail(code=404, msg="对象不存在").dict(by_alias=True),
                        status_code=status.HTTP_404_NOT_FOUND)


async def mysql_operational_error(_: Request, exc: MysqlOperationalError):
    """    mysql 数据库异常错误处理    """
    log.error(f"数据库 OperationalError 异常 {str(exc)}")
    return JSONResponse(RespFail(code=500, msg="数据操作失败").dict(by_alias=True),
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def http_error_handler(_: Request, exc: HTTPException):
    """    http异常处理    """
    log.error(f"http异常处理 {exc.status_code=} {exc.detail=}")
    if exc.status_code == 401:
        return JSONResponse(RespFail(code=401, msg=exc.detail).dict(by_alias=True),
                            status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(RespFail(code=exc.status_code, msg=exc.detail, data=exc.detail).dict(by_alias=True),
                        status_code=exc.status_code, headers=exc.headers)


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError], ) -> JSONResponse:
    """    参数校验错误处理    """
    log.error(f"参数校验错误处理[422] {exc.errors()=}")
    return JSONResponse(RespFail(code=422, msg="数据校验错误").dict(by_alias=True),
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, )


def register_exceptions(app: FastAPI) -> FastAPI:
    """注册异常信息"""
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(MysqlConnectionError, mysql_connection_error)
    app.add_exception_handler(MysqlDoesNotExist, mysql_does_not_exist)
    app.add_exception_handler(MysqlIntegrityError, mysql_integrity_error)
    app.add_exception_handler(MysqlValidationError, mysql_validation_error)
    app.add_exception_handler(MysqlOperationalError, mysql_operational_error)
    app.add_exception_handler(RedisConnectionError, redis_connection_error)
    return app
