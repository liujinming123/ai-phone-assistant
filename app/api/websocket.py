from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.session_manager import SessionManager
from app.services.audio_processor import AudioProcessor
from app.services.vad_service import VADService
from app.services.model_client import ModelServiceClient
from app.services.call_manager import CallManager
from app.config import settings
from loguru import logger
import time
import wave
import os

router = APIRouter()
session_manager = SessionManager()
audio_processor = AudioProcessor()
vad_service = VADService()
call_manager = CallManager()

@router.websocket("/call/{call_id}")
async def websocket_call_endpoint(websocket: WebSocket, call_id: str):
    """WebSocket音频流端点"""
    await websocket.accept()
    logger.info(f"WebSocket连接建立: {call_id}")
    
    session = await session_manager.create_session(
        call_id,
        "你是AI客服，请友善地与用户对话"
    )
    
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
            audio_data = await websocket.receive_bytes()
            
            processed = audio_processor.process_chunk(audio_data, source_sr=8000)
            
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
                
                if is_speaking and silence_counter > silence_threshold:
                    is_speaking = False
                    
                    full_audio = b''.join(audio_buffer)
                    await session_manager.model_client.send_audio(
                        session.remote_session_id,
                        full_audio
                    )
                    
                    response_audio_buffer = []
                    async for response_chunk in session_manager.model_client.stream_response(
                        session.remote_session_id
                    ):
                        await websocket.send_bytes(response_chunk)
                        response_audio_buffer.append(response_chunk)
                    
                    if settings.save_audio_output and response_audio_buffer:
                        os.makedirs(settings.audio_output_dir, exist_ok=True)
                        timestamp = int(time.time())
                        output_path = os.path.join(
                            settings.audio_output_dir,
                            f"response_{call_id}_{timestamp}.wav"
                        )
                        full_response_audio = b''.join(response_audio_buffer)
                        with wave.open(output_path, "wb") as wav_file:
                            wav_file.setnchannels(settings.audio_channels)
                            wav_file.setsampwidth(settings.audio_bit_depth // 8)
                            wav_file.setframerate(settings.audio_sample_rate)
                            wav_file.writeframes(full_response_audio)
                        
                        logger.info(f"音频已保存: {output_path}")
                    
                    audio_buffer = []
                    
                    conversation = await session_manager.model_client.get_conversation(
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
