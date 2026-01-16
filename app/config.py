from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000
    max_concurrent_calls: int = 10
    
    # 远程模型服务
    remote_model_service_url: str
    remote_model_service_api_key: str
    remote_model_service_timeout: int = 30
    
    # 音频配置
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    audio_bit_depth: int = 16
    audio_buffer_size: int = 3200
    
    # 音频输出配置
    save_audio_output: bool = True
    audio_output_dir: str = "/cpfs/user/zhaochenxu1/users/liujinming/git_program/mp3"
    
    # VAD配置
    vad_aggressiveness: int = 2
    vad_frame_duration: int = 30
    silence_duration: int = 800
    
    # 阿里云配置
    aliyun_access_key_id: str
    aliyun_access_key_secret: str
    aliyun_call_center_region: str = "cn-hangzhou"
    aliyun_call_center_instance_id: str
    
    # 日志配置
    log_level: str = "INFO"
    log_dir: str = "./logs"
    
    # 数据库
    database_url: str = "sqlite:///./database/conversations.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        protected_namespaces = ()

settings = Settings()
