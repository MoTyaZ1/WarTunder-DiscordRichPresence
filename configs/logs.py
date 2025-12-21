# configs/logs.py
import logging
import sys
import os
import json

class ColoredFormatter(logging.Formatter):
    """Colored formatter for logs"""
    
    def __init__(self):
        """Formatter initialization"""
        fmt = '%(levelname)s - %(message)s'
        super().__init__(fmt=fmt)
        
        # Импортируем цвета один раз при инициализации
        try:
            from configs.colors import COLORS as COLORS_IMPORTED
            self.COLORS = COLORS_IMPORTED
        except ImportError:
            # Если модуль цветов не найден, отключаем цвета
            self.COLORS = {
                'DEBUG': '',
                'INFO': '',
                'WARNING': '',
                'ERROR': '',
                'CRITICAL ERROR': '',
                'RESET': '',
                'DISCORD': '',
                'SUCCESS': '',
                'CHECK': ''
            }
    
    def format(self, record):
        # Преобразуем CRITICAL в CRITICAL ERROR для форматирования
        if record.levelname == 'CRITICAL':
            record.levelname = 'CRITICAL ERROR'
            
        # Save original format
        log_message = super().format(record)
        
        # Add color to log level
        if record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS.get('RESET', '')
            
            # Replace only level with colored version
            level_with_color = f"{color}{record.levelname}{reset}"
            log_message = log_message.replace(record.levelname, level_with_color, 1)
        
        return log_message

def init_logger():
    """Logger initialization with console output only"""
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, log_level, logging.INFO)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove old handlers
    logger.handlers.clear()
    
    # ONLY console handler (with color)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    # Выводим сообщение о инициализации логгера с переводом
    try:
        from configs.colors import colored_text
        from configs.translations import get_translation
        
        # Получаем язык из настроек
        lang = "en"  # значение по умолчанию
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
                    lang = settings_data.get("lang", "en")
        except:
            pass
        
        # Получаем перевод
        message = get_translation(lang, "logger_initialized")
        info_text = colored_text("INFO", "INFO")
        
        # Выводим напрямую в консоль, а не через logger
        print(f"{info_text} - {message}")
        
    except ImportError as e:
        # Fallback если модули не доступны
        print(f"INFO - Logger initialized (level: {log_level})")
    except Exception as e:
        # Любая другая ошибка
        print(f"INFO - Logger initialized (level: {log_level})")
    
    return logger

# Functions for logging status
def log_presence_struct(state: str, details: str, large_img: str, 
                       large_text: str, small_img: str, small_text: str):
    """Logging status structure"""
    logger = logging.getLogger(__name__)
    logger.info(f"State: {state}")
    logger.info(f"Details: {details}")
    logger.info(f"Large image: {large_img}")
    logger.info(f"Large text: {large_text}")
    logger.info(f"Small image: {small_img}")
    logger.info(f"Small text: {small_text}")

def error_log_presence_struct(err: Exception, state: str, details: str, 
                            large_img: str, large_text: str, 
                            small_img: str, small_text: str):
    """Logging error when setting status"""
    logger = logging.getLogger(__name__)
    error_msg = str(err)
    # Берем только первую часть сообщения об ошибке
    if ':' in error_msg:
        error_msg = error_msg.split(':')[0]
    elif '(' in error_msg:
        error_msg = error_msg.split('(')[0].strip()
    
    logger.error(f"Error setting status: {error_msg}")

def error_log(details: str, err: Exception):
    """Error logging"""
    logger = logging.getLogger(__name__)
    error_msg = str(err)
    # Берем только первую часть сообщения об ошибке
    if ':' in error_msg:
        error_msg = error_msg.split(':')[0]
    elif '(' in error_msg:
        error_msg = error_msg.split('(')[0].strip()
    
    logger.error(f"{details}: {error_msg}")