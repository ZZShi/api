from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import settings


# -----------------------数据库配置-----------------------------------
DB_ORM_CONFIG = {
    "connections": {
        "base": {
            'engine': 'tortoise.backends.sqlite',
            "credentials": {
                # 'host': settings.MYSQL_HOST,
                # 'user': settings.MYSQL_USER,
                # 'password': settings.MYSQL_PWD,
                # 'port': settings.MYSQL_PORT,
                # 'database': settings.MYSQL_DB,
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
        "base": {"models": ["models.base"], "default_connection": "base"}
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    # 注册数据库
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )
