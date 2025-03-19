"""
@Des:视图路由
"""
from fastapi import APIRouter,Request,Form
#from models.base import Users
#from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from views.home import register,register_result,test_sc,enter,enter_result,dogtest,test,admin
viewsrouter=APIRouter(tags=["视图路由"])
viewsrouter.get("/register",response_class=HTMLResponse)(register)
viewsrouter.post("/register/result",response_class=HTMLResponse)(register_result)
viewsrouter.get("/cookie",response_class=HTMLResponse)(test_sc)
viewsrouter.get("/enter",response_class=HTMLResponse)(enter)
viewsrouter.post("/enter/result",response_class=HTMLResponse)(enter_result)
viewsrouter.get("/dog",response_class=HTMLResponse)(dogtest)
viewsrouter.get("/admin",response_class=HTMLResponse)(admin)    