from typing import Dict, List
from datetime import datetime
from app.models.conversation import Conversation, Message
from app.services.model_client import ModelServiceClient
from loguru import logger

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Conversation] = {}
        self.model_client = ModelServiceClient()
        
    async def create_session(
        self, 
        call_id: str, 
        system_prompt: str = ""
    ) -> Conversation:
        """创建会话"""
        try:
            remote_session_id = await self.model_client.create_session(
                system_prompt
            )
            
            session = Conversation(
                call_id=call_id,
                remote_session_id=remote_session_id,
                system_prompt=system_prompt,
                created_at=datetime.now()
            )
            
            self.sessions[call_id] = session
            logger.info(f"会话创建成功: {call_id}")
            return session
            
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            raise
    
    def get_session(self, call_id: str) -> Conversation:
        """获取会话"""
        return self.sessions.get(call_id)
    
    def update_history(
        self, 
        call_id: str, 
        messages: List[Message]
    ):
        """更新对话历史"""
        if call_id in self.sessions:
            self.sessions[call_id].messages.extend(messages)
            self.sessions[call_id].updated_at = datetime.now()
    
    async def cleanup_session(self, call_id: str):
        """清理会话"""
        if call_id in self.sessions:
            del self.sessions[call_id]
            logger.info(f"会话已清理: {call_id}")
