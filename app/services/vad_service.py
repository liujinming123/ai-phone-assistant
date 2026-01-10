import numpy as np
from app.config import settings
from loguru import logger

class VADService:
    def __init__(self):
        self.energy_threshold = 1000  # 能量阈值
        self.silence_threshold = settings.silence_duration
        self.frame_duration_ms = 30
        self.sample_rate = settings.audio_sample_rate
        self.frame_size = int(
            self.frame_duration_ms * 
            self.sample_rate * 2 / 1000
        )
        
    def is_speech(self, audio_chunk: bytes) -> bool:
        """判断是否包含语音（基于能量检测）"""
        try:
            if len(audio_chunk) < self.frame_size:
                return False
            
            audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
            energy = np.sqrt(np.mean(audio_array.astype(float)**2))
            
            return energy > self.energy_threshold
            
        except Exception as e:
            logger.error(f"VAD检测失败: {e}")
            return False
    
    def detect_speech_end(self, audio_buffer: list) -> bool:
        """检测语音结束（静音）"""
        if len(audio_buffer) == 0:
            return True
        
        silence_samples = int(
            self.silence_threshold * 
            self.sample_rate * 2 / 1000
        )
        
        recent_audio = b''.join(audio_buffer[-min(10, len(audio_buffer)):])
        return len(recent_audio) < silence_samples
