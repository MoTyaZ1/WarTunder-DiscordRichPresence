import json
import logging
import sys
import os
from dataclasses import dataclass
from typing import Optional
import requests

logger = logging.getLogger(__name__)

@dataclass
class PresenceSettings:
    """Settings for Discord presence"""
    refresh_time: int
    large_img: str
    alt_presence: bool
    lang: str
    vehicle_details: bool
    left_tank_state: str
    right_tank_state: str
    left_air_state: str
    right_air_state: str
    debug_mode: bool = False

def get_base_path():
    """Get base path for both script and EXE"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_default_settings() -> PresenceSettings:
    """Get default settings"""
    return PresenceSettings(
        refresh_time=7,
        large_img="main_logo",
        alt_presence=False,
        lang="en",
        vehicle_details=True,
        left_tank_state="speed",
        right_tank_state="crew",
        left_air_state="spd",
        right_air_state="alt",
        debug_mode=False
    )

def init_presence_settings() -> PresenceSettings:
    """Initialize presence settings"""
    try:
        base_path = get_base_path()
        settings_path = os.path.join(base_path, "settings.json")
        
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return PresenceSettings(
                refresh_time=data.get("refresh_time", 7),
                large_img=data.get("large_img", "main_logo"),
                alt_presence=data.get("alt_presence", False),
                lang=data.get("lang", "en"),
                vehicle_details=data.get("vehicle_details", True),
                left_tank_state=data.get("left_tank_state", "speed"),
                right_tank_state=data.get("right_tank_state", "crew"),
                left_air_state=data.get("left_air_state", "spd"),
                right_air_state=data.get("right_air_state", "alt"),
                debug_mode=data.get("debug_mode", False)
            )
    except FileNotFoundError:
        logger.warning("settings.json not found, using default settings")
        return get_default_settings()
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing settings.json: {e}")
        return get_default_settings()
    except Exception as e:
        logger.error(f"Error loading settings: {e}")
        return get_default_settings()

def init_http_client() -> requests.Session:
    """Initialize HTTP client"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "WarThunder-Rich-Presence/1.0",
        "Accept": "application/json",
        "Connection": "keep-alive"
    })
    return session