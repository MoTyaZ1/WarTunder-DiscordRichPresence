# configs/colors.py
"""
Цветовая схема для консольного вывода
"""

# ANSI color codes
COLORS = {
    # Уровни логирования
    'DEBUG': '\033[94m',           # Синий
    'INFO': '\033[37m',            # Белый
    'WARNING': '\033[93m',         # Желтый
    'ERROR': '\033[91m',           # Ярко-красный
    'CRITICAL ERROR': '\033[31m',  # Темно-красный
    
    # Специальные категории
    'DISCORD': '\033[94m',         # Синий (для сообщений Discord)
    'SUCCESS': '\033[92m',         # Зеленый (для успешных операций)
    'CHECK': '\033[37m',           # Белый (для проверок)
    
    # Технические
    'RESET': '\033[0m'             # Сброс цвета
}

def colored_text(text: str, color_name: str) -> str:
    """Получить текст с цветом по имени цвета"""
    color_code = COLORS.get(color_name, COLORS['RESET'])
    return f"{color_code}{text}{COLORS['RESET']}"

def get_color_code(color_name: str) -> str:
    """Получить только код цвета"""
    return COLORS.get(color_name, COLORS['RESET'])