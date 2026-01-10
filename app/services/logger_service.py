from loguru import logger
from app.config import settings
import os
from datetime import datetime

class LoggerService:
    def __init__(self):
        self.setup_logger()
        
    def setup_logger(self):
        """配置日志系统"""
        # 确保日志目录存在
        os.makedirs(settings.log_dir, exist_ok=True)
        
        # 移除默认处理器
        logger.remove()
        
        # 添加控制台日志
        logger.add(
            sink=lambda msg: print(msg, end=''),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=settings.log_level,
            colorize=True
        )
        
        # 添加文件日志
        log_file = os.path.join(
            settings.log_dir, 
            f"assistant_{datetime.now().strftime('%Y%m%d')}.log"
        )
        logger.add(
            sink=log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=settings.log_level,
            rotation="1 day",
            retention="7 days",
            encoding="utf-8"
        )
        
        logger.info("日志系统初始化完成")
    
    def save_conversation(self, call_id: str, conversation):
        """保存对话记录"""
        try:
            log_file = os.path.join(
                settings.log_dir, 
                f"conversation_{call_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            with open(log_file, 'w', encoding='utf-8') as f:
                import json
                json.dump({
                    "call_id": call_id,
                    "timestamp": datetime.now().isoformat(),
                    "conversation": conversation
                }, f, ensure_ascii=False, indent=2)
            
            logger.info(f"对话记录已保存: {log_file}")
            
        except Exception as e:
            logger.error(f"保存对话记录失败: {e}")

logger_service = LoggerService()
