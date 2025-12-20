"""
Инициализация модуля types
"""
from .map import MapStruct
from .info import MainInfoStruct
from .air import IndicatorsAirStruct
from .ground import IndicatorsGroundStruct

__all__ = [
    'MapStruct',
    'MainInfoStruct', 
    'IndicatorsAirStruct',
    'IndicatorsGroundStruct'
]