from fastapi import Request,Form,Cookie
from tortoise import Tortoise,connections
from fastapi.responses import JSONResponse
from tortoise.expressions import Q
import redis
from core.validator import CreateUser
from typing import Optional
redis_client = redis.Redis(host='localhost', port=6379, db=0)
from models.base import Users,Role  # 添加模型导入
#管理员页面
async def admin(request:Request):
    """
    :param request: 请求
    :return: 返回管理员页面
    """
    return request.app.state.views.TemplateResponse("admin.html",{"request":request})
#注册页面
async def register(request:Request):
    """
    :param request: 请求
    :return: 返回注册页面
    """
    return request.app.state.views.TemplateResponse("reg.html",{"request":request})
#登录页面
async def enter(request:Request):
    """
    :param request: 请求
    :return: 返回登陆页面
    """
    return request.app.state.views.TemplateResponse("enter.html",{"request":request})
#登录结果页面
async def enter_result(request:Request,username:str=Form(...),password:str=Form(...)):
    """
    :param request: 请求
    :param username: 用户名
    :param password: 密码
    :return: 返回登陆结果页面
    """
    # 查询所有用户
    print("用户:",username)
    print("密码:",password)
    #conn = Tortoise.get_connection("base")
    #result = await conn.execute_query_dict("SHOW TABLES;")
    #print("result:",result)
    
    user = await Users.get_or_none(Q(name=username) & Q(passwd=password))
    sym=False
    if user:
        message = f"{username},登录成功！欢迎回来 😊"
        success = True
        userid=user.id
        user_role = await Role.filter(user__id=userid).values("role_name")
        if user_role and any(role["role_name"] == "admin" for role in user_role):
            print("用户角色:",user_role)
            sym=True
    else:
        message = "用户名或密码错误，请重试！"
        success = False
    return request.app.state.views.TemplateResponse("enter_result.html",{"request":request,"name":username,"message":message,"success":success,"sym":sym})
#登录结果页面

#注册结果页面
async def register_result(request:Request,username:str=Form(...),password:str=Form(...)):
    """
    :param request: 请求
    :param username: 用户名
    :param password: 密码
    :return: 返回注册结果页面
    """
    # 创建新用户
    new=CreateUser(username=username,password=password)
    newuser=await  Users.create(name=new.username, passwd=new)
    print("新用户:",newuser)
    # 查询所有用户
    """
    user_list = await Users.all()
    for user in user_list:
        print("用户:",user.name)
        print("密码:",user.passwd)
        print("用户类型:",user.typee)
        print("昵称:",user.nickname)
        print("创建时间:",user.create_time)
        print("更新时间:",user.update_time)"""
    return request.app.state.views.TemplateResponse("regresult.html",{"request":request,"name":username,"password":password})

#测试页面
async def dogtest(request:Request):
    """
    :param request: 请求
    :return: 返回测试页面
    """
    return request.app.state.views.TemplateResponse("dog.html",{"request":request})

#cookie测试
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response

#cookie and session 测试
async def test_sc(request:Request,session_id:Optional[str]=Cookie(None)):
    """
    :param request: 请求
    :return: 返回测试cookie页面
    """
    cookie=session_id
    session=request.session.get("session")
    page_data={
        "cookie":cookie,
        "session":session
    }
    request.session.setdefault("232323","fake-cookie-session-value")
    return request.app.state.views.TemplateResponse("t_cose.html",{"request":request,**page_data})

async def test():
    return {"message":"a test"}

