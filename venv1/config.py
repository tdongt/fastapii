"""
@Des:基本配置文件
"""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
import os
class config(BaseSettings):
    load_dotenv(find_dotenv(),override=False)
    APP_DEBUG: bool = True
    static_path: str = os.path.join(os.getcwd(), 'static')
    template_path: str = os.path.join(static_path, 'templates')
    SECRET_KEY : str = "session"
    SESSION_COOKIE : str = "session_id"
    SESSION_MAX_AGE : int = 1
      # Jwt
    JWT_SECRET_KEY : str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM : str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES : int = 24 * 60
    #SWAGGER_UI_OAUTH2_REDIRECT_URL : str = "/api/v1/test/oath2"
    #跨域请求
    CORS_ORIGINS : list = ["http://10.81.29.195:8000","http://192.168.1.107:8000","http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    #14 * 24 * 60 * 60