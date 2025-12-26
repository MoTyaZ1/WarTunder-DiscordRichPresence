# discord/types/info.py
from dataclasses import dataclass

@dataclass
class MainInfoStruct:
    """Основная структура информации о технике"""
    army_type: str = ""
    vehicle_game_name: str = ""
    crew_total: float = 0.0
    crew_current: float = 0.0
    speed: float = 0.0
    rpm: float = 0.0  # Добавлено для оборотов двигателя