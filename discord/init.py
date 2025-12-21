# discord/init.py
import logging
import time
import pypresence
from pypresence.exceptions import DiscordNotFound, InvalidID

# Импортируем новую функцию colored_text
try:
    from configs.colors import colored_text
except ImportError:
    def colored_text(text: str, color_name: str) -> str:
        return text

logger = logging.getLogger(__name__)
_rpc_client = None
_start_time = None

def connect_discord_rpc(discord_code: str, lang: str = "en"):
    """Connect to Discord RPC"""
    global _rpc_client, _start_time
    
    # Импортируем функцию перевода
    from configs.translations import get_translation
    t = lambda key: get_translation(lang, key)
    
    _start_time = int(time.time())
    
    if _rpc_client is not None:
        try:
            _rpc_client.clear_activity()
            _rpc_client.close()
        except:
            pass
        _rpc_client = None
    
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            discord_text = colored_text("DISCORD", "DISCORD")
            print(f"{discord_text} - {t('discord_connecting')}{attempt + 1}")
            
            # Новый способ подключения
            _rpc_client = pypresence.Client(discord_code)
            _rpc_client.start()
            
            # Test update with main_logo
            _rpc_client.set_activity(
                state="Starting",
                details="War Thunder",
                large_image="main_logo",
                large_text="War Thunder",
                start=_start_time
            )
            
            print(f"{discord_text} - {t('discord_connected')} ({t('app_id')}: {discord_code})")
            return True
            
        except DiscordNotFound:
            if attempt < max_attempts - 1:
                wait = 2 * (attempt + 1)
                discord_text = colored_text("DISCORD", "DISCORD")
                print(f"{discord_text} - {t('discord_not_found')}, {t('discord_waiting')} {wait} {t('discord_seconds')}")
                time.sleep(wait)
            else:
                discord_text = colored_text("DISCORD", "DISCORD")
                print(f"{discord_text} - {t('discord_not_found')}")
                return False
                
        except InvalidID:
            discord_text = colored_text("DISCORD", "DISCORD")
            print(f"{discord_text} - {t('discord_invalid_id')}: {discord_code}")
            return False
            
        except Exception as e:
            error_msg = str(e)
            if attempt < max_attempts - 1:
                wait = 2 * (attempt + 1)
                
                # Try with fallback image
                if "large_image" in error_msg or "image" in error_msg.lower():
                    discord_text = colored_text("DISCORD", "DISCORD")
                    print(f"{discord_text} - {t('discord_image_problem')}")
                    try:
                        if _rpc_client:
                            _rpc_client.set_activity(
                                state="War Thunder",
                                details="Rich Presence",
                                large_image="war_thunder",
                                large_text="Game",
                                start=_start_time
                            )
                            print(f"{discord_text} - {t('discord_alt_success')}")
                            return True
                    except Exception as retry_error:
                        discord_text = colored_text("DISCORD", "DISCORD")
                        print(f"{discord_text} - {t('discord_retry_failed')}: {retry_error}")
                
                discord_text = colored_text("DISCORD", "DISCORD")
                print(f"{discord_text} - {t('discord_connection_error')}, {t('discord_waiting')} {wait} {t('discord_seconds')}")
                time.sleep(wait)
            else:
                discord_text = colored_text("DISCORD", "DISCORD")
                print(f"{discord_text} - {t('discord_failed_attempts')} {max_attempts} {t('discord_attempts')}")
                return False
    
    return False

def get_start_time():
    """Get application start time"""
    global _start_time
    if _start_time is None:
        _start_time = int(time.time())
    return _start_time

def get_rpc_client():
    """Get RPC client"""
    global _rpc_client
    
    if _rpc_client is None:
        raise RuntimeError("Discord RPC not initialized")
    
    return _rpc_client

def close_rpc():
    """Close RPC connection"""
    global _rpc_client, _start_time
    if _rpc_client is not None:
        try:
            _rpc_client.clear_activity()
            _rpc_client.close()
        except Exception as e:
            pass
        finally:
            _rpc_client = None
            _start_time = None