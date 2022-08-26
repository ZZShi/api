from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from common.logger import log
from config import settings


# -----------------------数据库配置-----------------------------------
DB_ORM_CONFIG = {
    "connections": {
        "base": {
            'engine': 'tortoise.backends.sqlite',
            "credentials": {
                'file_path': "db.sqlite"
            }
        },
        # "base": {
        #     'engine': 'tortoise.backends.mysql',
        #     "credentials": {
        #         'host': settings.MYSQL_HOST,
        #         'user': settings.MYSQL_USER,
        #         'password': settings.MYSQL_PWD,
        #         'port': settings.MYSQL_PORT,
        #         'database': settings.MYSQL_DB,
        #     }
        # }
    },
    "apps": {
        "base": {"models": ["aerich.models", "models.base"], "default_connection": "base"}
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    # 注册数据库
    log.debug(f"连接数据库：{DB_ORM_CONFIG['connections']['base']}")
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )


async def close_connection():
    log.debug(f"断开数据库：{DB_ORM_CONFIG['connections']['base']}")
    await Tortoise.close_connections()
