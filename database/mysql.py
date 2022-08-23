from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import settings


# -----------------------数据库配置-----------------------------------
DB_ORM_CONFIG = {
    "connections": {
        # "base": {
        #     'engine': 'tortoise.backends.sqlite',
        #     "credentials": {
        #         'host': settings.MYSQL_HOST,
        #         'user': settings.MYSQL_USER,
        #         'password': settings.MYSQL_PWD,
        #         'port': settings.MYSQL_PORT,
        #         'database': settings.MYSQL_DB,
        #         'file_path': settings.BASE_DIR
        #     }
        # },
        "base": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': settings.MYSQL_HOST,
                'user': settings.MYSQL_USER,
                'password': settings.MYSQL_PWD,
                'port': settings.MYSQL_PORT,
                'database': settings.MYSQL_DB,
            }
        },
        # "db2": {
        #     'engine': 'tortoise.backends.mysql',
        #     "credentials": {
        #         'host': os.getenv('DB2_HOST', '127.0.0.1'),
        #         'user': os.getenv('DB2_USER', 'root'),
        #         'password': os.getenv('DB2_PASSWORD', '123456'),
        #         'port': int(os.getenv('DB2_PORT', 3306)),
        #         'database': os.getenv('DB2_DB', 'db2'),
        #     }
        # },
        # "db3": {
        #     'engine': 'tortoise.backends.mysql',
        #     "credentials": {
        #         'host': os.getenv('DB3_HOST', '127.0.0.1'),
        #         'user': os.getenv('DB3_USER', 'root'),
        #         'password': os.getenv('DB3_PASSWORD', '123456'),
        #         'port': int(os.getenv('DB3_PORT', 3306)),
        #         'database': os.getenv('DB3_DB', 'db3'),
        #     }
        # },

    },
    "apps": {
        "base": {"models": ["models.base"], "default_connection": "base"},
        # "db2": {"models": ["models.db2"], "default_connection": "db2"},
        # "db3": {"models": ["models.db3"], "default_connection": "db3"}
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
