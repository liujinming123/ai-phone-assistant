from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.call_manager import CallManager
from app.services.session_manager import SessionManager
from app.services.logger_service import logger_service
from loguru import logger

router = APIRouter()
call_manager = CallManager()
session_manager = SessionManager()

class CallInitiateRequest(BaseModel):
    phone_number: str
    prompt: str = "你是AI客服，请友善地与用户对话"

@router.post("/call/initiate")
async def initiate_call(request: CallInitiateRequest):
    """发起呼叫"""
    try:
        call = await call_manager.initiate_call(
            request.phone_number,
            request.prompt
        )
        
        logger.info(f"呼叫发起: {call['call_id']} -> {request.phone_number}")
        
        return call
        
    except Exception as e:
        logger.error(f"发起呼叫失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/call/{call_id}")
async def get_call_status(call_id: str):
    """查询呼叫状态"""
    status = call_manager.get_call_status(call_id)
    if not status:
        raise HTTPException(status_code=404, detail="呼叫不存在")
    
    return status

@router.post("/call/{call_id}/terminate")
async def terminate_call(call_id: str):
    """结束呼叫"""
    try:
        await call_manager.terminate_call(call_id)
        return {"call_id": call_id, "status": "terminated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/call/{call_id}/conversation")
async def get_conversation(call_id: str):
    """获取对话记录"""
    session = session_manager.get_session(call_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return {
        "call_id": call_id,
        "conversation": session.messages
    }
