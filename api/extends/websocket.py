"""
@Des: websocket通信
"""
import json
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jwt import PyJWTError
from pydantic import ValidationError
import jwt
from config import config
from models.base import Users
from schemas.validator import WebsocketMessage
from typing import Any
settings = config()
webrouter = APIRouter()
# 用户验证
def check_token(token: str):
    """
    用户验证
    :param token
    :return: 用户ID 或 None
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("user_id")
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, PyJWTError, ValidationError):
        return None

# WebSocket 处理类
class WebSocketHandler:
    online_conn = []
    encoding = "json"
    async def on_connect(self, websocket: WebSocket):
        """处理 WebSocket 连接"""
        await websocket.accept()
        token = websocket.headers.get("Authorization")
        user_id = check_token(token)
        if not user_id:
            await websocket.close()
            return

        # 移除旧连接
        """self.online_conn = [conn for conn in self.online_conn if conn["user_id"] != user_id]
        self.online_conn.append({"user_id": user_id, "conn": websocket})"""

        # 发送在线用户列表
        on_users = await Users.filter(id__in=[conn["user_id"] for conn in self.online_conn]).values("id", "username")
        data = {"action": "refresh_online_user", "data": on_users}
        for conn in self.online_conn:
            await conn["conn"].send_json(data)

    async def on_receive(self, websocket: WebSocket, data: Any):
        """处理 WebSocket 消息"""
        token = websocket.headers.get("Authorization")
        user_id = check_token(token)
        if not user_id:
            await websocket.close()
            return

        try:
            msg = WebsocketMessage(**data)
            if msg.action == "push_msg":
                msg.action = "pull_msg"
                msg.user = user_id
                for conn in self.online_conn:
                    await conn["conn"].send_json(msg.dict())
        except Exception as e:
            print(f"消息处理错误: {e}")

    async def on_disconnect(self, websocket: WebSocket):
        """处理 WebSocket 断开"""
        self.online_conn = [conn for conn in self.online_conn if conn["conn"] != websocket]

        # 更新在线用户列表
        on_users = await Users.filter(id__in=[conn["user_id"] for conn in self.online_conn]).values("id", "username")
        data = {"action": "refresh_online_user", "data": on_users}
        for conn in self.online_conn:
            await conn["conn"].send_json(data)

# WebSocket 路由
websocket_handler = WebSocketHandler()

@webrouter.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端点"""
    await websocket_handler.on_connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket_handler.on_receive(websocket, data)
    except WebSocketDisconnect:
        await websocket_handler.on_disconnect(websocket)

