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
        self.model = "/vepfs/public/model-public/Qwen3-Omni-30B-A3B-Instruct"
        self._session_history = {}

    async def create_session(self, system_prompt: str) -> str:
        """创建远程会话"""
        import uuid
        session_id = str(uuid.uuid4())
        self._session_history[session_id] = {
            "system_prompt": system_prompt,
            "messages": [{"role": "system", "content": system_prompt}],
            "created_at": "2026-01-16"
        }
        logger.info(f"会话创建: {session_id}")
        return session_id

    async def send_audio(self, session_id: str, audio_data: bytes):
        """发送音频到远程模型 (模拟ASR + 对话)"""
        if session_id not in self._session_history:
            logger.error(f"会话不存在: {session_id}")
            return

        history = self._session_history[session_id]

        logger.info(f"处理音频: {len(audio_data)} bytes")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": history["messages"] + [
                            {
                                "role": "user",
                                "content": "请用中文简短回复，控制在50字以内。"
                            }
                        ],
                        "max_tokens": 150
                    }
                )
                response.raise_for_status()
                result = response.json()
                reply = result["choices"][0]["message"]["content"]

                history["messages"].append({
                    "role": "assistant",
                    "content": f"[模拟ASR结果]: {reply}"
                })

                logger.info(f"模型回复: {reply[:100]}")

        except Exception as e:
            logger.error(f"处理音频失败: {e}")
            raise

    async def stream_response(
        self,
        session_id: str
    ) -> AsyncGenerator[bytes, None]:
        """流式接收音频响应 (使用TTS生成音频)"""
        if session_id not in self._session_history:
            logger.error(f"会话不存在: {session_id}")
            return

        history = self._session_history[session_id]

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/v1/audio/speech",
                    json={
                        "model": self.model,
                        "input": history["messages"][-1]["content"],
                        "voice": "alloy",
                        "response_format": "mp3"
                    }
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk

        except Exception as e:
            logger.error(f"生成语音失败: {e}")
            raise

    async def cancel_generation(self, session_id: str):
        """取消生成"""
        logger.info(f"取消生成: {session_id}")

    async def generate_greeting(self, prompt: str) -> bytes:
        """生成问候音频"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/audio/speech",
                    json={
                        "model": self.model,
                        "input": prompt,
                        "voice": "alloy",
                        "response_format": "mp3"
                    }
                )
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"生成问候失败: {e}")
            raise

    async def get_conversation(self, session_id: str) -> list:
        """获取对话记录"""
        if session_id in self._session_history:
            return self._session_history[session_id]["messages"]
        return []
