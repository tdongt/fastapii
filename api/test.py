from typing import Any,List,Dict
from core.response import success, fail
from schemas.validator import CreateUser,AccountLogin,UserInfo,CreateRole,CreateAccess,ControlRole,UpdateAccess
from models.base import Users, Role, Access
from core.Utils import en_password,check_password
from core.auth import create_access_token #导入创建token的函数
from fastapi.responses import JSONResponse

async def user_info(user_id: int):
    """
    获取用户信息
    :param user_id: int
    :return:
    """
    print("在搞用户数据 稍等...")
    user_data = await Users.get_or_none(pk=user_id)
    if user_data.user_status == 0:
        user_data.user_status = '禁用'
    else:user_data.user_status = '正常'
    if user_data.typee == 0:
        user_data.typee = '普通用户'
    else:user_data.typee = '根管理员'
    
    user_dict = {
        "id": user_data.id,
        "name": user_data.name,
        "nickname": user_data.nickname,
        "email": user_data.email,
        "phone": user_data.phone,
        "user_status": user_data.user_status,
        "typee": user_data.typee,
        "header_img": user_data.header_img
    }
    if not user_data:
        return fail(msg=f"用户ID{user_id}不存在!")
    return success(msg="用户信息", data=user_dict)


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
    return JSONResponse({
        "code": 200,
        "message": "登陆成功😄",
        "data": {"token": jwt_token,
                 "id": get_user.pk}
    }, status_code=200, headers={"Set-Cookie": "X-token=Bearer "+jwt_token})



async def get_roles():
    """获取所有角色数据"""
    roles = await Role.all().prefetch_related("access")
    roles_data = [
        {
            "id": role.id,
            "role_name": role.role_name,
            "role_status": role.role_status,
            "role_desc": role.role_desc,
            "access": [
                {"id": acc.id, "access_name": acc.access_name, "scopes": acc.scopes}
                for acc in role.access
            ]
        }
        for role in roles
    ]
    return success(msg="角色列表", data=roles_data)

async def add_role(post: CreateRole):
    """添加角色"""
    create_role = await Role.create(
        role_name=post.role_name,
        role_status=post.role_status,
        role_desc=post.role_desc,
    )
    if post.access:
        access_instances = await Access.filter(id__in=post.access)  # 查找符合的权限对象
        if not access_instances:
            return fail(msg="权限不存在")
        await create_role.access.add(*access_instances)
    if not create_role:
        return fail(msg=f"角色{post.role_name}创建失败!")
    return success(msg=f"角色{create_role.role_name}创建成功")
async def control_role(post: ControlRole):
    """
    控制角色
    修改角色权限
    更新角色状态（删除或禁用,启用）
    - action="delete" -> 删除角色
    - action="disable" -> 禁用角色
    - action="enable" -> 启用角色
    - action="add" -> 增加权限
    - action="remove" -> 移除权限
    """
    # 查询角色是否存在
    role = await Role.filter(id=post.role_id).first()
    if not role:
        return {"code": 404, "message": "角色不存在"}

    if post.action == "delete":
        # 删除角色，并清理关联的 ManyToMany 关系
        await role.access.clear()  # 清除关联权限
        await role.delete()
        return {"code": 200, "message": f"角色 {role.role_name} 已删除"}

    elif post.action == "disable":
        # 禁用角色
        role.role_status = False
        await role.save()
        return {"code": 200, "message": f"角色 {role.role_name} 已禁用"}
    elif post.action == "enable":
        # 启用角色
        role.role_status = True
        await role.save()
        return {"code": 200, "message": f"角色 {role.role_name} 已启用"}
    
    # 处理权限增加
    elif post.action == "add":
        new_accesses = await Access.filter(id__in=post.access).all()
        if len(new_accesses) != len(post.access):
            return {"code": 400, "message": "部分权限不存在，请检查"}
        await role.access.add(*new_accesses)  # 增加新权限
    # 处理权限删除
    elif post.action == "remove":
        remove_accesses = await Access.filter(id__in=post.access).all()
        if len(remove_accesses) != len(post.access):
            return {"code": 400, "message": "部分权限不存在，请检查"}
        await role.access.remove(*remove_accesses)  # 移除指定权限
    else:
        return {"code": 400, "message": "无效操作，请使用 'delete' 或 'disable' 或 'enable'"}
    #返回处理结果
    return {
        "code": 200,
        "message": f"角色 {role.role_name} 权限已更新",
        "added": post.access or [],
        "removed": post.access or []
    }
#查询权限并以树型返回
async def get_access_tree() -> List[Dict[str, Any]]:
    """
    查询所有权限数据，并构建权限树
    """
    acs = await Access.all()
    access_dict = {ac.id: ac for ac in acs}
    # 添加 children 字段
    for ac in access_dict.values():
        ac.children = []
    # 构建树
    root = []
    for ac in access_dict.values():
        if ac.parent_id and ac.parent_id in access_dict:
           access_dict[ac.parent_id].children.append(ac)
        else:
            root.append(ac)

    return serialize_Accesss(root)

def serialize_Accesss(Access_list):
    """
    递归将 ORM 对象转换为 JSON 结构
    """
    return [
        {
            "id": ac.id,
            "access_name": ac.access_name,
            "scopes": ac.scopes,
            "access_desc": ac.access_desc,
            "children": serialize_Accesss(ac.children) if ac.children else []
        }
        for ac in Access_list
    ]
async def update_access(post: UpdateAccess):
    """
    对权限进行修改,更新
    post.access_id: int 权限ID
    post.access_scopes: list[int] 权限范围
    post.action: str 操作类型

    - action="delete" -> 删除权限
    - action="disable" -> 开启权限验证
    - action="enable" -> 关闭权限验证
    """
    # 查询权限是否存在
    access = await Access.filter(id=post.access_id).first()
    if not access:
        return {"code": 404, "message": "权限不存在"}
    if post.action == "delete":
        #没有设置清除关联,返回与权限关联的角色,提醒更新者
        #查询所有拥有该权限的角色
        roles_with_access = await Role.filter(access__id=post.access_id).values("id", "role_name")
        if roles_with_access:
            return {
                "code": 400,
                "message": "无法删除，该权限仍然绑定以下角色，请先解绑:",
                "roles": roles_with_access
            }
        await access.delete()
        return {"code": 200, "message": f"权限 {access.access_name} 已删除"}
    elif post.action == "disable":
        # 关闭验证
        access.is_check = False
        await access.save()
        return {"code": 200, "message": f"权限 {access.access_name} 已禁用"}
    elif post.action == "enable":
        # 开启验证
        access.is_check = True
        await access.save()
        return {"code": 200, "message": f"权限 {access.access_name} 已启用"}
    else:
        return {"code": 400, "message": "无效操作，请使用 'delete' 或 'disable' 或 'enable'"}
    

    