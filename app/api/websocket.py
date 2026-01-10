from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.session_manager import SessionManager
from app.services.audio_processor import AudioProcessor
from app.services.vad_service import VADService
from app.services.model_client import ModelServiceClient
from app.services.call_manager import CallManager
from app.config import settings
from loguru import logger
import time

router = APIRouter()
session_manager = SessionManager()
audio_processor = AudioProcessor()
vad_service = VADService()
model_client = ModelServiceClient()
call_manager = CallManager()

@router.websocket("/ws/call/{call_id}")
async def websocket_call_endpoint(websocket: WebSocket, call_id: str):
    """WebSocket音频流端点"""
    await websocket.accept()
    logger.info(f"WebSocket连接建立: {call_id}")
    
    # 创建会话
    session = await session_manager.create_session(
        call_id,
        "你是AI客服，请友善地与用户对话"
    )
    
    # 连接音频流
    call_stream = call_manager.connect_audio_stream(call_id)
    
    audio_buffer = []
    is_speaking = False
    silence_counter = 0
    silence_threshold = int(
        settings.silence_duration * 
        settings.audio_sample_rate * 2 / 1000
    )
    
    try:
        while True:
            # 接收音频
            audio_data = await websocket.receive_bytes()
            
            # 预处理（假设来源是8kHz）
            processed = audio_processor.process_chunk(audio_data, source_sr=8000)
            
            # VAD检测
            if vad_service.is_speech(processed):
                silence_counter = 0
                
                if not is_speaking:
                    is_speaking = True
                    await websocket.send_json({
                        "type": "speech_start",
                        "timestamp": int(time.time())
                    })
                
                audio_buffer.append(processed)
                
            else:
                silence_counter += len(processed)
                
                # 检测语音结束
                if is_speaking and silence_counter > silence_threshold:
                    is_speaking = False
                    
                    # 发送音频到模型
                    full_audio = b''.join(audio_buffer)
                    await model_client.send_audio(
                        session.remote_session_id,
                        full_audio
                    )
                    
                    # 流式接收响应
                    async for response_chunk in model_client.stream_response(
                        session.remote_session_id
                    ):
                        await websocket.send_bytes(response_chunk)
                    
                    audio_buffer = []
                    
                    # 更新历史
                    conversation = await model_client.get_conversation(
                        session.remote_session_id
                    )
                    session_manager.update_history(call_id, conversation)
                    
                    await websocket.send_json({
                        "type": "turn_complete",
                        "timestamp": int(time.time())
                    })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket断开: {call_id}")
    except Exception as e:
        logger.error(f"WebSocket错误: {e}")
    finally:
        await session_manager.cleanup_session(call_id)
