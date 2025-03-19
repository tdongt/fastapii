"""
@Des:基本路由
"""
from fastapi import APIRouter,Request,Form,Security
from api.test import login,zc,user_info,user_del,user_add,get_user_rules,account_login
from config import config
from starlette.responses import HTMLResponse
from core.auth import check_permissions
apirouter=APIRouter(prefix="/api",tags=["api路由"])
@apirouter.get("/")
async def index():
    return {"message":"Hello World","data":[{'name':'张三','age':18},{'name':'李四','age':20}]}
apirouter.get("/login",summary="登陆接口")(login)
apirouter.post("/注册",summary="注册接口")(zc)
apirouter.post("/user/account/login", tags=["用户接口"], summary="用户登陆")(account_login)
apirouter.get("/adminuserinfo",
              tags=["用户管理"],
              summary="获取当前用户信息",
              dependencies=[Security(check_permissions)],
              )(user_info)
apirouter.delete("/adminuserdel",
                 tags=["用户管理"],
                 summary="用户删除",
                 dependencies=[Security(check_permissions, scopes=["user_delete"])],
                 )(user_del)

apirouter.post("/adminuseradd",
               tags=["用户管理"],
               summary="用户添加",
               dependencies=[Security(check_permissions, scopes=["user_add","user_list"])]
               )(user_add)

apirouter.get("/adminuserrules",
              tags=["用户管理"],
              summary="查询用户权限",
              dependencies=[Security(check_permissions, scopes=["user_add"])]
              )(get_user_rules)

