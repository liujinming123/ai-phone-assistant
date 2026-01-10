from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    audio_url: Optional[str] = None
    timestamp: Optional[datetime] = None

class Conversation(BaseModel):
    call_id: str
    remote_session_id: str
    system_prompt: str
    messages: List[Message] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
