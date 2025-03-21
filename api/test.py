from pydantic import BaseModel
from core.response import success, fail
from core.validator import CreateUser,AccountLogin,UserInfo
from models.base import Users, Role, Access
from core.Utils import en_password,check_password
from core.auth import create_access_token #导入创建token的函数
from fastapi.responses import JSONResponse
class zcl(BaseModel):
    name:str
    age:int
    zxtime:str
async def login(name: str=None,password:str=None):
    return {"data":[{'name':name,'password':password}]}
async def zc(person:zcl):
    return {"data":[{'name':person.name,'age':person.age,'zxtime':person.zxtime}]}
async def user_info(user_id: int):
    """
    获取用户信息
    :param user_id: int
    :return:
    """
    user_data = await Users.get_or_none(pk=user_id)
    if not user_data:
        return fail(msg=f"用户ID{user_id}不存在!")
    return success(msg="用户信息", data=user_data)


async def user_add(post: CreateUser):
    """
    创建用户
    :param post: CreateUser
    :return:
    """
    post.password = en_password(post.password)
    create_user = await Users.create(name=post.account, passwd=post.password)
    if not create_user:
        return fail(msg=f"用户{post.account}创建失败!")
    return success(msg=f"用户{create_user.name}创建成功")


async def user_del(user_id: int):
    """
    删除用户
    :param user_id: int
    :return:
    """
    delete_user = await Users.filter(pk=user_id).delete()
    if not delete_user:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功")


async def get_user_rules(user_id: int):
    """
    获取用户权限集合
    :param user_id:
    :return:
    """

    # 查询当前用户拥有的角色
    user_role = await Role.filter(user__id=user_id).values("role_name")
    # 查询当前用户的所有权限
    user_access_list = await Access.filter(role__user__id=user_id, is_check=True).values("id", "scopes")
    # 验证当前用户对当前域是否有权限
    is_pass = await Access.get_or_none(role__user__id=user_id, is_check=True, scopes="article_push", role__role_status=True)
    data = {
        "user_role": user_role,
        "pass": True if is_pass else False,
        "user_access_list": user_access_list
    }
    return success(msg="用户权限", data=data)
async def account_login(post: AccountLogin):
    print("执行了")
    """
    获取用户权限集合
    :param user_id:
    :return:
    用户登陆
    :param post:
    :return: jwt token
    """
    get_user = await Users.get_or_none(name=post.account)
    print(get_user)
    if not get_user:
        return fail(msg=f"用户{post.account}密码验证失败!")
    if not check_password(post.password, get_user.passwd):
        return fail(msg=f"用户{post.account}密码验证失败!")
    if not get_user.user_status:
        return fail(msg=f"用户{post.account}已被管理员禁用!")
    jwt_data = {
        "user_id": get_user.pk,
        "user_type": get_user.typee
    }
    jwt_token = create_access_token(data=jwt_data)
    # return success(msg="登陆成功😄", data={"token": jwt_token})
    return JSONResponse({
        "code": 200,
        "message": "登陆成功😄",
        "data": {}
    }, status_code=200, headers={"Set-Cookie": "X-token=Bearer "+jwt_token})