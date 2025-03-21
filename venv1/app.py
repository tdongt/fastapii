# -*- coding:utf-8 -*-
"""
@Created on : 2025.3.1
@Author: anit
@Des: app运行时文件
"""
from fastapi import FastAPI,Request,HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from config import config
from api.base import apirouter
from views.base import viewsrouter
from core import events
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from core.middleware import BaseMiddleware
from tortoise.exceptions import OperationalError, DoesNotExist
from core.exception import http_error_handler, http422_error_handler, unicorn_exception_handler, UnicornException, \
    mysql_operational_error, mysql_does_not_exist
settings=config()
""" app = FastAPI(
    debug=settings.APP_DEBUG,
    docs_url=None,
    redoc_url=None,
    #swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL,
) """
app=FastAPI(title="一个fastapi",description="欢迎来到这个孩子的fastapi",version="0.0.1")
@app.get("/",tags=["打招呼路由"])
async def read_root(request:Request):
    """
    :param request: 请求
    :return: 返回首页
    """
    return app.state.views.TemplateResponse("first.html",{"request":request})   
app.include_router(viewsrouter)
app.include_router(apirouter)
app.mount("/static",StaticFiles(directory="static"),name="static")
app.state.views=Jinja2Templates(directory=settings.template_path)
#添加中间件
app.add_middleware(BaseMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE,
    max_age=settings.SESSION_MAX_AGE
)
#跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
#事件监听
app.add_event_handler("startup", events.startup(app))
app.add_event_handler("shutdown", events.stopping(app))
# 异常错误处理
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.add_exception_handler(UnicornException, unicorn_exception_handler)
app.add_exception_handler(DoesNotExist, mysql_does_not_exist)
app.add_exception_handler(OperationalError, mysql_operational_error)

