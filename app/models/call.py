from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Call(BaseModel):
    call_id: str
    phone_number: str
    status: str
    prompt: str
    created_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[int] = None
