import os
from pathlib import Path
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        # 环境变量文件
        env_file = ".env.prod" if os.getenv('PROJECT_ENV') == 'prod' else ".env.dev"

    # 环境配置: dev prod
    project_env: str = "dev"

    # debug模式
    debug: bool = True if project_env == 'dev' else False

    # 项目标题
    project_title = 'FastAPI 后端'
    # 项目描述
    project_description = '一个牛逼的API后端'
    # 项目版本
    project_version = '0.0.1'

    # url的前缀
    url_prefix: str = "/api/v1"
    # host
    server_host: str = 'localhost'
    server_port: int = 8000

    # 是否启用 /test 接口
    enable_test_router: bool = True

    #  swagger docs 的登陆重定向地址
    swagger_ui_oauth2_redirect_url: str = url_prefix + '/test/token'

    # 项目根目录
    base_dir = Path(__file__).absolute().parent.parent.parent
    # 日志目录
    log_dir = base_dir / 'logs'
    # 静态资源
    static_dir = base_dir / 'static'
    static_url_prefix: str = '/static'
    # 用户上传目录
    media_dir = base_dir / 'media'
    media_url_prefix: str = '/media'
    # jinja2 模板目录
    jinja2_templates_dir = static_dir / 'templates'

    # 中间件配置
    # 跨域请求
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["PUT", 'POST', 'GET', 'DELETE', 'OPTIONS']
    cors_allow_headers: List[str] = ["*"]
    # Session
    session_secret_key = "sadehewagbwft34ba"
    session_cookie = "session_id"
    session_max_age = 14 * 24 * 60 * 60
    # SetSessionMiddleware
    session_cookie_name = 'session'
    # 日志中间件的白名单，只填写去除 url_prefix 的部分
    logger_path_white_list: List[str] = ['/user/captcha', '/test/files', '/test/uploadfile']
    # TrustedHostMiddleware
    allowed_hosts = ["*"]

    # 数据库
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str

    # redis
    cache_redis_url: str

    # captcha
    # 图片验证码有效时间
    captcha_seconds: int = 5 * 60
    # 图片验证码key
    captcha_key: str = 'captcha:{}'

    # jwt加密的盐
    jwt_secret_key: str
    # jwt加密算法
    jwt_algorithm: str = 'HS256'
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 7 * 24 * 60 * 60

    @property
    def tortoise_orm_model_modules(self) -> List[str]:
        return ['aerich.models', 'backend.models']

    @property
    def tortoise_orm_config(self) -> dict:
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": self.mysql_host,
                        "port": self.mysql_port,
                        "user": self.mysql_user,
                        "password": self.mysql_password,
                        "database": self.mysql_database,
                        }
                    }
                },
            "apps": {
                "base": {
                    "models": self.tortoise_orm_model_modules,
                    "default_connection": "default"
                    }
                },
            'use_tz': False,
            'timezone': 'Asia/Shanghai'
            }


settings = Settings()


if __name__ == '__main__':
    print(settings.mysql_host)
    print(settings.mysql_password)
