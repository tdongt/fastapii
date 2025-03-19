
"""
@Des:事件监听
"""
from tortoise import Tortoise
from typing import Callable
from fastapi import FastAPI
from database.mysql import register_mysql
from database.redis import sys_cache, code_cache
from redis.asyncio import Redis
from database.mysql import DB_ORM_CONFIG
def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """
    async def app_start() -> None:
        # APP启动完成后触发
        print("fastapi已启动")
        # 注册数据库
        await register_mysql(app)
        await Tortoise.init(config=DB_ORM_CONFIG)
        await Tortoise.generate_schemas()
        print("mysql已连接")
        # 注入缓存到app state
        app.state.cache = await sys_cache()
        app.state.code_cache = await code_cache()

        pass
    return app_start
def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """
    async def stop_app() -> None:
        # APP停止时触发
        print("fastapi已停止")
        cache: Redis = await app.state.cache
        code: Redis = await app.state.code_cache
        await cache.close()
        await code.close()

    return stop_app