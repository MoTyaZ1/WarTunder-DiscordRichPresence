# main.py
import sys
import os
import traceback

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
script_dir = base_path
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, 'configs'))
sys.path.insert(0, os.path.join(script_dir, 'discord'))
sys.path.insert(0, os.path.join(script_dir, 'game'))

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
                import json
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
        
        # Загружаем переводы напрямую из файла
        try:
            # Импортируем translations.py как модуль
            import importlib.util
            translations_path = os.path.join(script_dir, "configs", "translations.py")
            spec = importlib.util.spec_from_file_location("translations", translations_path)
            translations_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(translations_module)
            t = lambda key: translations_module.get_translation(language, key)
        except Exception as e:
            print(f"Ошибка загрузки переводов: {e}")
            t = lambda key: key
        
        # Загружаем цвета напрямую
        try:
            colors_path = os.path.join(script_dir, "configs", "colors.py")
            spec = importlib.util.spec_from_file_location("colors", colors_path)
            colors_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(colors_module)
            colored_text = colors_module.colored_text
        except Exception as e:
            print(f"Ошибка загрузки цветов: {e}")
            def colored_text(text: str, color_name: str) -> str:
                return text
        
        success_text = colored_text("SUCCESS", "SUCCESS")
        error_text = colored_text("ERROR", "ERROR")
        
        # Проверка файлов
        settings_path = os.path.join(base_path, "settings.json")
        if not os.path.exists(settings_path):
            print(f"{t('creating_file')}")
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
                print(f"{success_text} {t('file_created')}")
            except Exception as e:
                print(f"{error_text} - {t('loading_error')} {e}")
                input(f"\n{t('press_enter')}")
                return
        else:
            print(f"{success_text} settings.json")
        
        # Импортируем остальные модули напрямую
        try:
            # settings.py
            settings_py_path = os.path.join(script_dir, "configs", "settings.py")
            spec = importlib.util.spec_from_file_location("settings", settings_py_path)
            settings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings_module)
            
            # logs.py
            logs_py_path = os.path.join(script_dir, "configs", "logs.py")
            spec = importlib.util.spec_from_file_location("logs", logs_py_path)
            logs_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logs_module)
            
            # Импортируем остальные модули
            sys.path.insert(0, script_dir)
            import game.api as game_api
            
            # discord модули
            import discord.handler as handler_module
            import discord.init as discord_init_module
            
            # Сохраняем ссылки
            settings = settings_module
            logs = logs_module
            handler = handler_module
            discord_init = discord_init_module
            api = game_api
            
        except ImportError as e:
            print(f"\n{error_text} - Error importing modules: {e}")
            print(f"{t('check_files_location')}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
            sys.exit(1)
        
        # Инициализация настроек
        try:
            # Передаем base_path в init_presence_settings
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