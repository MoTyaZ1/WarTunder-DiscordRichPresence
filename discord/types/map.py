from dataclasses import dataclass

@dataclass
class MapStruct:
    """Структура информации о карте"""
    valid: bool = False
    game_running: bool = False