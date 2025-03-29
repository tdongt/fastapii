# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 5:29 PM
@Author: binkuolo
@Des: 用户验证模型
"""
from pydantic import Field, BaseModel
from typing import Optional,Any
# 创建用户
class CreateUser(BaseModel):
    account: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=8, max_length=12)
    #user_type: bool = Field(default=False)
# 创建角色
class CreateRole(BaseModel):
    role_name: str = Field(min_length=3, max_length=10)
    role_status: bool = Field(default=False)
    role_desc: Optional[str]
    access: Optional[list[int]] = []
# 创建权限
class CreateAccess(BaseModel):
    access_name: str = Field(min_length=3, max_length=10)
    parent_id: int = Field(default=0)
    scopes: str = Field(min_length=3, max_length=10)
    access_desc: Optional[str]
    menu_icon: Optional[str]
    is_check: bool = Field(default=False)
    is_menu: bool = Field(default=False)
# 用户登录
class AccountLogin(BaseModel):
    account: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=8, max_length=12)

# 用户信息
class UserInfo(BaseModel):
    id: int
    account: str
    age: Optional[int]
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    user_status: bool
    header_img: Optional[str]
    sex: int

# 控制角色
class ControlRole(BaseModel):
    role_id : int
    action : str
    access : Optional[list[int]] = []
# 更新权限
class UpdateAccess(BaseModel):
    access_id : int
    access_scopes : Optional[list[int]] = []
    action : str
    parent_id : int

class WebsocketMessage(BaseModel):
    action: Optional[str]
    user: Optional[int]
    data: Optional[Any]