# main.py
import sys
import os
import traceback
import json

# ВКЛЮЧЕНИЕ ПОДДЕРЖКИ ЦВЕТОВ ДЛЯ WINDOWS
def enable_windows_colors():
    """Включает поддержку ANSI цветов в консоли Windows"""
    if sys.platform != "win32":
        return True  # Для не-Windows систем цвета уже работают
    
    # Способ 1: Самый простой и часто работающий метод
    os.system("")
    
    # Способ 2: Используем Windows API для надежности
    try:
        import ctypes
        
        # Определяем константы
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        ENABLE_PROCESSED_OUTPUT = 0x0001
        ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
        
        # Получаем handle консоли
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        
        # Получаем текущий режим
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            # Устанавливаем новый режим с поддержкой виртуального терминала
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING | ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT
            kernel32.SetConsoleMode(handle, new_mode)
            return True
    except Exception:
        # Если не получилось - продолжаем без цветов
        pass
    
    return False

# Включаем цвета при запуске
enable_windows_colors()

# Получаем базовый путь (одинаково для всех модулей)
def get_base_path():
    """Get base path for both script and EXE"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Добавляем все подпапки в sys.path
base_path = get_base_path()
sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path, 'configs'))
sys.path.insert(0, os.path.join(base_path, 'discord'))
sys.path.insert(0, os.path.join(base_path, 'game'))

# Простая функция для цветов на случай если модуль не загрузится
def simple_colored_text(text: str, color_name: str) -> str:
    """Простая заглушка для цветного текста"""
    color_codes = {
        'SUCCESS': '\033[92m',    # Зеленый
        'ERROR': '\033[91m',      # Красный
        'INFO': '\033[37m',       # Белый
        'WARNING': '\033[93m',    # Желтый
        'CRITICAL ERROR': '\033[31m',  # Темно-красный
        'DISCORD': '\033[94m',    # Синий
        'CHECK': '\033[37m',      # Белый
    }
    reset = '\033[0m'
    color = color_codes.get(color_name, '')
    return f"{color}{text}{reset}"

# Глобальная переменная для языка
_current_language = "ru"

def set_language(lang: str):
    """Установить текущий язык"""
    global _current_language
    _current_language = lang

def load_language_from_settings():
    """Загрузить язык из settings.json"""
    try:
        settings_path = os.path.join(base_path, "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang = data.get("lang", "ru")
                return lang
    except:
        pass
    return "ru"

def main():
    """Основная функция"""
    try:
        # Сначала загружаем язык из settings.json
        language = load_language_from_settings()
        set_language(language)
        
        # Используем простую функцию для цветов на старте
        colored_text = simple_colored_text
        success_text = colored_text("SUCCESS", "SUCCESS")
        error_text = colored_text("ERROR", "ERROR")
        
        # Проверка файлов
        settings_path = os.path.join(base_path, "settings.json")
        if not os.path.exists(settings_path):
            print("Creating settings.json...")
            try:
                with open(settings_path, "w", encoding="utf-8") as f:
                    f.write(f'''{{
  "refresh_time": 7,
  "large_img": "main_logo",
  "alt_presence": false,
  "lang": "{language}",
  "vehicle_details": true,
  "left_tank_state": "speed",
  "right_tank_state": "crew",
  "left_air_state": "spd",
  "right_air_state": "alt"
}}''')
                print(f"{success_text} settings.json created")
            except Exception as e:
                print(f"{error_text} - Error loading settings.json: {e}")
                input("\nPress Enter to exit...")
                return
        else:
            print(f"{success_text} settings.json")
        
        # Пытаемся импортировать модули
        t = lambda key: key  # временная функция перевода
        
        try:
            # Пробуем импортировать как модули из папки configs
            from configs import settings as settings_module
            from configs import logs as logs_module
            from configs import translations as translations_module
            from configs import colors as colors_module
            
            # Пробуем использовать функцию из colors_module если она есть
            try:
                colored_text = colors_module.colored_text
                success_text = colored_text("SUCCESS", "SUCCESS")
                error_text = colored_text("ERROR", "ERROR")
            except:
                pass  # Оставляем простую версию
            
            # Устанавливаем функцию перевода
            t = lambda key: translations_module.get_translation(language, key)
            
            # Импортируем остальные модули
            from game import api as game_api
            from discord import handler as handler_module
            from discord import init as discord_init_module
            
            # Сохраняем ссылки
            settings = settings_module
            logs = logs_module
            handler = handler_module
            discord_init = discord_init_module
            api = game_api
            
        except ImportError as e:
            print(f"Import error: {e}")
            traceback.print_exc()
            
            # Пробуем альтернативный способ импорта
            try:
                # Добавляем пути в sys.path
                for folder in ['configs', 'discord', 'game']:
                    folder_path = os.path.join(base_path, folder)
                    if os.path.exists(folder_path) and folder_path not in sys.path:
                        sys.path.insert(0, folder_path)
                
                # Пробуем импортировать снова с полными путями
                import importlib
                
                # Динамически импортируем модули
                settings_spec = importlib.util.spec_from_file_location(
                    "settings", 
                    os.path.join(base_path, "configs", "settings.py")
                )
                settings_module = importlib.util.module_from_spec(settings_spec)
                sys.modules["settings"] = settings_module
                settings_spec.loader.exec_module(settings_module)
                
                logs_spec = importlib.util.spec_from_file_location(
                    "logs", 
                    os.path.join(base_path, "configs", "logs.py")
                )
                logs_module = importlib.util.module_from_spec(logs_spec)
                sys.modules["logs"] = logs_module
                logs_spec.loader.exec_module(logs_module)
                
                translations_spec = importlib.util.spec_from_file_location(
                    "translations", 
                    os.path.join(base_path, "configs", "translations.py")
                )
                translations_module = importlib.util.module_from_spec(translations_spec)
                sys.modules["translations"] = translations_module
                translations_spec.loader.exec_module(translations_module)
                
                colors_spec = importlib.util.spec_from_file_location(
                    "colors", 
                    os.path.join(base_path, "configs", "colors.py")
                )
                colors_module = importlib.util.module_from_spec(colors_spec)
                sys.modules["colors"] = colors_module
                colors_spec.loader.exec_module(colors_module)
                
                # Пробуем использовать функцию из colors_module
                try:
                    colored_text = colors_module.colored_text
                    success_text = colored_text("SUCCESS", "SUCCESS")
                    error_text = colored_text("ERROR", "ERROR")
                except:
                    pass
                
                t = lambda key: translations_module.get_translation(language, key)
                
                # Импортируем остальные модули
                api_spec = importlib.util.spec_from_file_location(
                    "game_api", 
                    os.path.join(base_path, "game", "api.py")
                )
                game_api = importlib.util.module_from_spec(api_spec)
                sys.modules["game_api"] = game_api
                api_spec.loader.exec_module(game_api)
                
                handler_spec = importlib.util.spec_from_file_location(
                    "handler", 
                    os.path.join(base_path, "discord", "handler.py")
                )
                handler_module = importlib.util.module_from_spec(handler_spec)
                sys.modules["handler"] = handler_module
                handler_spec.loader.exec_module(handler_module)
                
                init_spec = importlib.util.spec_from_file_location(
                    "discord_init", 
                    os.path.join(base_path, "discord", "init.py")
                )
                discord_init_module = importlib.util.module_from_spec(init_spec)
                sys.modules["discord_init"] = discord_init_module
                init_spec.loader.exec_module(discord_init_module)
                
                settings = settings_module
                logs = logs_module
                handler = handler_module
                discord_init = discord_init_module
                api = game_api
                
            except Exception as e2:
                print(f"\n{error_text} - Critical import error: {e2}")
                traceback.print_exc()
                input("\nPress Enter to exit...")
                sys.exit(1)
        
        # Инициализация настроек
        try:
            app_settings = settings.init_presence_settings(base_path)
        except Exception as e:
            print(f"\n{error_text} - Error initializing settings: {e}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
            sys.exit(1)
        
        # Обновляем язык на основе окончательных настроек
        set_language(app_settings.lang)
        
        # Инициализация логгера
        try:
            logs.init_logger()
        except Exception as e:
            print(f"\n{error_text} - Error initializing logger: {e}")
            traceback.print_exc()
        
        # Инициализация HTTP клиента
        try:
            http_client = settings.init_http_client()
        except Exception as e:
            print(f"\n{error_text} - Error initializing HTTP client: {e}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
            sys.exit(1)
        
        # Подключение к Discord
        try:
            if not discord_init.connect_discord_rpc("1450643150811955282", app_settings.lang):
                input(f"\n{t('press_enter')}")
                return
        except Exception as e:
            print(f"\n{error_text} - Error connecting to Discord: {e}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
            return
        
        # Информация о запуске
        info_text = colored_text("INFO", "INFO")
        print(f"\n{info_text} - {t('program_started')}")
        
        # Предупреждение - 16 попыток по 10 секунд
        yellow_warning = colored_text("WARNING", "WARNING")
        print(f"\n{yellow_warning} - {t('program_will_try')}")
        
        # Запуск основного цикла
        try:
            handler.run_update_presence_loop(app_settings, http_client)
        except KeyboardInterrupt:
            print("\n\nProgram stopped by user")
        except Exception as e:
            critical_error = colored_text("CRITICAL ERROR", "CRITICAL ERROR")
            print(f"\n\n{critical_error} - {e}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
        
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user")
    except Exception as e:
        critical_error = colored_text("CRITICAL ERROR", "CRITICAL ERROR")
        print(f"\n\n{critical_error} - {e}")
        traceback.print_exc()
        input(f"\nPress Enter to exit...")

if __name__ == "__main__":
    main()