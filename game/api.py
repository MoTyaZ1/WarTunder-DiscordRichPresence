# game/api.py
import json
import logging
import time
from typing import Optional, Tuple
import requests

# Определяем структуры локально, чтобы избежать циклических импортов
class MapStruct:
    def __init__(self, valid=False, game_running=False):
        self.valid = valid
        self.game_running = game_running

class MainInfoStruct:
    def __init__(self, army_type="", vehicle_game_name="", crew_total=0.0, crew_current=0.0, speed=0.0, rpm=0.0):
        self.army_type = army_type
        self.vehicle_game_name = vehicle_game_name
        self.crew_total = crew_total
        self.crew_current = crew_current
        self.speed = speed
        self.rpm = rpm

logger = logging.getLogger(__name__)

# Global variables for tracking attempts
_connection_attempts = 0
_max_attempts = 16
_last_attempt_time = 0
_connection_failed = False

def _reset_connection_attempts():
    """Reset attempt counter"""
    global _connection_attempts, _last_attempt_time, _connection_failed
    _connection_attempts = 0
    _last_attempt_time = 0
    _connection_failed = False

def _increment_connection_attempts(lang: str = "en"):
    """Increment attempt counter and delay if needed"""
    global _connection_attempts, _last_attempt_time, _connection_failed
    
    if _connection_attempts > 0:
        # Каждая попытка ждет 10 секунд
        delay = 10
        try:
            from configs.translations import get_translation
            message = get_translation(lang, "attempt_waiting")
            logger.warning(message.format(attempt=_connection_attempts + 1, seconds=delay))
        except ImportError:
            logger.warning(f"Attempt #{_connection_attempts + 1}: waiting {delay} seconds...")
        time.sleep(delay)
    
    _connection_attempts += 1
    _last_attempt_time = time.time()
    
    if _connection_attempts >= _max_attempts:
        try:
            from configs.translations import get_translation
            message = get_translation(lang, "max_attempts_reached")
            logger.error(message)
        except ImportError:
            logger.error("Max connection attempts to War Thunder reached")
        _connection_failed = True
        return False
    
    return True

def check_connection_failed():
    """Check if max attempts reached"""
    return _connection_failed

def make_request(url: str, http_client, debug_mode: bool = False, lang: str = "en") -> Optional[requests.Response]:
    """Make HTTP request"""
    if debug_mode:
        logger.debug(f"Request to {url}")
    
    try:
        response = http_client.get(url, timeout=5)
        
        if debug_mode:
            logger.debug(f"Response from {url}: status {response.status_code}")
        
        if response.status_code != 200:
            logger.warning(f"Unexpected status code from {url}: {response.status_code}")
        
        # Если запрос успешен, сбрасываем счетчик попыток
        _reset_connection_attempts()
        response.raise_for_status()
        return response
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout when requesting {url}")
        if not _increment_connection_attempts(lang):
            return None
    except requests.exceptions.ConnectionError:
        try:
            from configs.translations import get_translation
            message = get_translation(lang, "connection_error")
            logger.error(message)
        except ImportError:
            logger.error("Connection error")
        if not _increment_connection_attempts(lang):
            return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e.response.status_code if hasattr(e, 'response') else 'Unknown'}")
        _reset_connection_attempts()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e).split(':')[0] if ':' in str(e) else 'Unknown error'}")
        _reset_connection_attempts()
    
    return None

def main_info_request(http_client, debug_mode: bool = False, lang: str = "en") -> Optional[MainInfoStruct]:
    """Request main vehicle information"""
    if check_connection_failed():
        return None
        
    response = make_request("http://127.0.0.1:8111/indicators", http_client, debug_mode, lang)
    if not response:
        return None
    
    try:
        data = response.json()
        
        if debug_mode:
            logger.debug(f"Main info data: {data}")
        
        return MainInfoStruct(
            army_type=data.get("army", ""),
            vehicle_game_name=data.get("type", ""),
            crew_total=float(data.get("crew_total", 0)),
            crew_current=float(data.get("crew_current", 0)),
            speed=float(data.get("speed", 0)),
            rpm=float(data.get("rpm", 0))
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Error in main_info_request: {e}")
    
    return None

def map_request(http_client, debug_mode: bool = False, lang: str = "en") -> MapStruct:
    """Request map information"""
    if check_connection_failed():
        return MapStruct(valid=False, game_running=False)
        
    response = make_request("http://127.0.0.1:8111/map_info.json", http_client, debug_mode, lang)
    
    if response is None:
        # Connection error - game not running or max attempts reached
        return MapStruct(valid=False, game_running=False)
    
    try:
        data = response.json()
        
        if debug_mode:
            logger.debug(f"Map data: {data}")
            
        # Game is running, return map validity
        return MapStruct(valid=data.get("valid", False), game_running=True)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Error in map_request: {e}")
    
    # If we got here, game is running but something went wrong
    return MapStruct(valid=False, game_running=True)

def air_state_request(http_client, debug_mode: bool = False, lang: str = "en") -> Tuple[bool, str]:
    """Request air vehicle state"""
    if check_connection_failed():
        return False, ""
        
    response = make_request("http://127.0.0.1:8111/state", http_client, debug_mode, lang)
    if not response:
        return False, ""
    
    try:
        text = response.text
        
        if debug_mode:
            logger.debug(f"Air state response length: {len(text)} characters")
            if len(text) < 500:  # Показываем короткие ответы полностью
                logger.debug(f"Air state content: {text}")
        
        return True, text
    except Exception as e:
        logger.error(f"Error in air_state_request: {e}")
    
    return False, ""