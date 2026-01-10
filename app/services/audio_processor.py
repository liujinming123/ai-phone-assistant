import numpy as np
from scipy import signal
from app.config import settings
from loguru import logger

class AudioProcessor:
    def __init__(self):
        self.target_sample_rate = settings.audio_sample_rate
        self.target_channels = settings.audio_channels
        self.target_bit_depth = settings.audio_bit_depth
        
    def process_chunk(
        self, 
        audio_data: bytes, 
        source_sr: int = 8000
    ) -> bytes:
        """处理音频块：重采样、归一化"""
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # 重采样
            if source_sr != self.target_sample_rate:
                num_samples = int(
                    len(audio_array) * self.target_sample_rate / source_sr
                )
                audio_array = signal.resample(
                    audio_array, num_samples
                ).astype(np.int16)
            
            audio_array = self._normalize(audio_array)
            return audio_array.tobytes()
            
        except Exception as e:
            logger.error(f"音频处理失败: {e}")
            raise
    
    def _normalize(self, audio_array: np.ndarray) -> np.ndarray:
        """音频归一化"""
        max_val = np.max(np.abs(audio_array))
        if max_val > 0:
            audio_array = (audio_array / max_val * 32767).astype(np.int16)
        return audio_array
    
    def combine_chunks(self, chunks: list) -> bytes:
        """合并音频块"""
        return b''.join(chunks)
