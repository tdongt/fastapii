"""
@Des: websocket通信
"""
import json
import time
from fastapi import APIRouter
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect
from jwt import PyJWTError
from pydantic import ValidationError
import jwt
from config import config
from models.base import Users
from schemas.validator import WebsocketMessage
from typing import Any
settings=config()
webrouter=APIRouter()

#用户验证
def check_token(token : str):
    """
    用户验证
    :param token
    :return:
    """
    try:
        payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])
        if payload:
            webid=payload.get("user_id",0)
            if webid==0:
                return False
        else:return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except (PyJWTError,ValidationError):
        return False
    return webid

#websocket处理类

class forsocket(WebSocketEndpoint):
    encoding = "json"
    online_conn = []
    #建立连接
    async def ws_connect(self,web_st : WebSocket):
        u_type = web_st.query_params.get("u_type")
        token = web_st.headers.get("sec-websocket-protocol")
        real_ip = web_st.headers.get('x-forwarded-for')
        real_host = web_st.headers.get("host")
        try:
            if not u_type or not token:
                raise WebSocketDisconnect
            user_id = check_token(token)
            if not user_id:
                raise WebSocketDisconnect
            await web_st.accept(subprotocol=token)
            #移除旧连接
            for con in self.online_conn:
                if con["user_id"] == user_id and con["u_type"] == u_type:
                    self.active_connections.remove(con)
            print(f"客户端ip:{real_ip} 来源:{real_host} type:{int(u_type)} ID: {int(user_id)}")
            #添加新连接
            self.online_conn.append(
                {
                    "user_id" : user_id,
                    "u_type" : u_type,
                    "con" : web_st
                }
            )
            #查询在线用户
            on_user = await Users.filter(id__in = [i['user_id'] for i in self.online_conn]).all().values("id","username")
            data = {
                "action": 'refresh_online_user',
                "data": on_user
            }
            time.sleep(1)
            for con in self.online_conn:
                await con['con'].send_json(data)
        except WebSocketDisconnect:
            await web_st.close()
            print("断开了连接")

    #消息接收
    async def ws_receive(self, web_st : WebSocket, data : Any):
        try:
            token = web_st.headers.get("Sec-Websocket-Protocol")
            user = check_token(token)
            if user:
                msg = WebsocketMessage(**msg)
                action = msg.action
                if action == "push_msg":
                    for i in self.online_conn:
                        msg.action = "pull_msg"
                        msg.user = user
                        await i['con'].send_json(msg.dict())
                else:raise WebSocketDisconnect
        except Exception as e:
            print(e)
    #断开连接
    async def ws_disconnect(self,web_st,close_conn):
        for con in self.online_conn:
            if con["con"] == web_st:
                self.online_conn.remove(con)
        on_user = await Users.filter(id__in=[i['user_id'] for i in self.online_conn]).all().values("id","username","header_img")
        data = {
            "action" : 'refresh_online_user',
            "data" : on_user
        }
        for con in self.online_conn:
            await con['con'].send_json(data)
    #消息发送
    async def send_msg(self,
                       web_st : WebSocket,
                       send_user : int,
                       send_type : int,
                       rece_user : int,
                       rece_type : int,
                       data : dict
                       ):
        """
        消息发送
        :param web_st: 发送者连接对象
        :param send_user: 发送者ID
        :param send_type: 发送者用户类型
        :param rece_user: 接收者用户ID
        :param rece_type: 接收者用户类型
        :param data: 要发送的数据
        :return:
        """
        user_on_state = False
        #寻找接收用户
        for con in self.online_conn:
            if con['user_id'] == rece_user and con['u_type'] == rece_type:
                user_on_state = True
                message = {
                    "send_user" : send_user,
                    "send_type" : send_type,
                    "data" : data
                }
                print(data)
                #发送消息
                await con['con'].send_text(json.dumps(message))
        if user_on_state:
            await web_st.send_text('{"send_status" : "send_success"}')
        else:
            await web_st.send_text('{"send_status" : "send_false"}')
webrouter.add_websocket_route('/test',forsocket)



        
