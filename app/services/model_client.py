import httpx
import asyncio
from typing import AsyncGenerator
from app.config import settings
from loguru import logger

class ModelServiceClient:
    def __init__(self):
        self.base_url = settings.remote_model_service_url
        self.api_key = settings.remote_model_service_api_key
        self.timeout = settings.remote_model_service_timeout
        
    async def create_session(self, system_prompt: str) -> str:
        """创建远程会话"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/session/create",
                    json={"system_prompt": system_prompt},
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()
                return response.json()["session_id"]
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            raise
    
    async def send_audio(self, session_id: str, audio_data: bytes):
        """发送音频到远程模型"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/session/{session_id}/audio",
                    content=audio_data,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "audio/pcm"
                    }
                )
                response.raise_for_status()
        except Exception as e:
            logger.error(f"发送音频失败: {e}")
            raise
    
    async def stream_response(
        self, 
        session_id: str
    ) -> AsyncGenerator[bytes, None]:
        """流式接收音频响应"""
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "GET",
                    f"{self.base_url}/api/session/{session_id}/stream",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk
        except Exception as e:
            logger.error(f"接收响应失败: {e}")
            raise
    
    async def cancel_generation(self, session_id: str):
        """取消生成（用于打断）"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                await client.post(
                    f"{self.base_url}/api/session/{session_id}/cancel",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
        except Exception as e:
            logger.error(f"取消生成失败: {e}")
    
    async def generate_greeting(self, prompt: str) -> bytes:
        """生成问候音频"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate/greeting",
                    json={"prompt": prompt},
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"生成问候失败: {e}")
            raise
    
    async def get_conversation(self, session_id: str) -> list:
        """获取对话记录"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/session/{session_id}/conversation",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()
                return response.json()["conversation"]
        except Exception as e:
            logger.error(f"获取对话记录失败: {e}")
            return []
