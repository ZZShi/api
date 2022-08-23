"""
请求响应返回格式封装
"""


def _RespBase(data=None, msg: str = "", code: int = 200):
    """基础返回格式"""
    result = {
        "code": code,
        "message": msg,
        "data": data if data else {}
    }
    return result


def RespSucc(data=None, msg: str = "请求成功", code: int = 200):
    """请求成功返回格式"""
    return _RespBase(data=data, code=code, msg=msg)


def RespFail(data=None, msg: str = "请求失败", code: int = -1):
    """请求失败返回格式"""
    return _RespBase(data=data, code=code, msg=msg)
