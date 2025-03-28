"""
@Des:基本路由
"""
from fastapi import APIRouter,Request,Form,Security
from api.test import user_info,user_del,user_add,get_user_rules,account_login,get_roles,add_role,control_role,get_access,update_access
from config import config
from starlette.responses import HTMLResponse
from core.auth import check_permissions
from api.extends import websocket
apirouter=APIRouter(prefix="/api")
apirouter.post("/user/account/login",
                tags=["用户接口"], 
                summary="用户登陆"
                )(account_login)
apirouter.get("/admin/user/info",
              tags=["用户管理"],
              summary="获取当前用户信息",
              #安全性检查
              #dependencies=[Security(check_permissions)],
              )(user_info)
apirouter.delete("/admin/user",
                 tags=["用户管理"],
                 summary="用户删除",
                 #安全性检查
                 #dependencies=[Security(check_permissions, scopes=["user_delete"])],
                 )(user_del)

apirouter.post("/admin/user",
               tags=["用户管理"],
               summary="用户添加",
               #安全性检查
               #dependencies=[Security(check_permissions, scopes=["user_add","user_list"])]
               )(user_add)

apirouter.get("/admin/user/access",
              tags=["用户管理"],
              summary="查询用户权限",
              #安全性检查
              #dependencies=[Security(check_permissions, scopes=["user_add"])]
              )(get_user_rules)

apirouter.get("/admin/role",
              tags=["角色管理"],
              summary="角色信息"
              )(get_roles)

apirouter.post("/admin/role",
               tags=["角色管理"],
               summary="添加角色"
               )(add_role)

apirouter.patch("/admin/role",
                tags=["角色管理"],
                summary="控制角色"
                )(control_role)

apirouter.get("/admin/access",
              tags=["权限管理"],
              summary="查询权限"
              )(get_access)

apirouter.patch("/admin/access",
               tags=["权限管理"],
               summary="修改权限"
               )(update_access)
apirouter.include_router(websocket.webrouter, 
                         prefix='/webst', 
                         tags=["WebSocket"])

