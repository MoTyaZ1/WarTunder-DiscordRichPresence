# main.py
import sys
import os
import traceback
import json
import importlib.util

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True

# Получаем базовый путь
def get_base_path():
    """Get base path for both script and EXE"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif hasattr(sys, '_MEIPASS'):
        # Для временной папки PyInstaller
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Глобальная переменная для базового пути
BASE_PATH = get_base_path()

# Функция для динамической загрузки модулей (РАБОТАЕТ С PYINSTALLER)
def load_module(module_name, file_path):
    """Динамически загружает модуль из файла"""
    try:
        # Если мы в EXE-режиме PyInstaller, импортируем напрямую
        if getattr(sys, 'frozen', False):
            # Пробуем импортировать обычным способом
            try:
                # Для configs модулей
                if module_name == "settings":
                    from configs import settings as module
                    return module
                elif module_name == "logs":
                    from configs import logs as module
                    return module
                elif module_name == "colors":
                    from configs import colors as module
                    return module
                elif module_name == "translations":
                    from configs import translations as module
                    return module
                # Для game модулей
                elif module_name == "game_api":
                    from game import api as module
                    return module
                # Для discord модулей
                elif module_name == "handler":
                    from discord import handler as module
                    return module
                elif module_name == "discord_init":
                    # Пробуем разные варианты
                    try:
                        from discord import rpc as module
                        return module
                    except ImportError:
                        try:
                            from discord import init as module
                            return module
                        except ImportError:
                            pass
            except ImportError as e:
                print(f"ImportError for {module_name}: {e}")
                # Пробуем альтернативный путь
                return None
        else:
            # Для обычного режима (не EXE) используем старый метод
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return None
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                print(f"Could not create spec for: {module_name}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"Error loading module {module_name}: {e}")
        return None

# Загружаем основные модули для цветов и переводов (УПРОЩЕННАЯ ВЕРСИЯ)
def load_essential_modules():
    """Загружает основные модули для работы программы"""
    modules = {}
    
    # Файлы для поиска
    files_to_find = {
        'translations': 'translations',
        'colors': 'colors',
        'settings': 'settings',
        'logs': 'logs',
    }
    
    # Пробуем загрузить каждый модуль
    for module_name, module_import_name in files_to_find.items():
        module_loaded = False
        
        try:
            # Пробуем импортировать как пакет configs
            module = __import__(f'configs.{module_import_name}', fromlist=[module_import_name])
            modules[module_name] = module
            module_loaded = True
        except ImportError:
            # Пробуем альтернативные пути
            if getattr(sys, 'frozen', False):
                # В EXE режиме
                try:
                    if hasattr(sys, '_MEIPASS'):
                        # Ищем во временной папке PyInstaller
                        search_paths = [
                            os.path.join(sys._MEIPASS, f"{module_import_name}.py"),
                            os.path.join(sys._MEIPASS, "configs", f"{module_import_name}.py"),
                            os.path.join(BASE_PATH, "configs", f"{module_import_name}.py"),
                        ]
                        
                        for file_path in search_paths:
                            if os.path.exists(file_path):
                                module = load_module(module_name, file_path)
                                if module:
                                    modules[module_name] = module
                                    module_loaded = True
                                    break
                except:
                    pass
        
        if not module_loaded:
            print(f"Warning: Could not load {module_name} module")
            modules[module_name] = None
    
    return modules

# Загружаем основные модули СРАЗУ (после определения функций)
essential_modules = load_essential_modules()

# Создаем простые заглушки если модули не загружены
class SimpleColors:
    @staticmethod
    def colored_text(text: str, color_name: str) -> str:
        return text

class SimpleTranslations:
    @staticmethod
    def get_translation(lang: str, key: str) -> str:
        return key

# Создаем глобальные переменные
_colors_module = essential_modules.get('colors') or SimpleColors()
_translations_module = essential_modules.get('translations') or SimpleTranslations()

# Глобальная переменная для языка
_current_language = "ru"

def set_language(lang: str):
    """Установить текущий язык"""
    global _current_language
    _current_language = lang

def load_language_from_settings():
    """Загрузить язык из settings.json"""
    try:
        settings_path = os.path.join(BASE_PATH, "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang = data.get("lang", "ru")
                return lang
    except:
        pass
    return "ru"

# Функция для цветного текста
def get_colored_text_func():
    """Получает функцию colored_text"""
    if hasattr(_colors_module, 'colored_text'):
        return _colors_module.colored_text
    else:
        return lambda text, color: text

# Функция для перевода
def get_translation_func(lang: str):
    """Получает функцию перевода"""
    if hasattr(_translations_module, 'get_translation'):
        return lambda key: _translations_module.get_translation(lang, key)
    else:
        return lambda key: key

def check_for_updates(lang: str = "en"):
    """Проверка обновлений через GitHub API"""
    try:
        import requests
        
        # Получаем функции перевода
        t = get_translation_func(lang)
        
        # Получаем функцию для цветов
        colored_text = get_colored_text_func()
        update_text = colored_text("UPDATE", "UPDATE") if colored_text("UPDATE", "UPDATE") != "UPDATE" else "UPDATE"
        check_text = colored_text("CHECK", "CHECK") if colored_text("CHECK", "CHECK") != "CHECK" else "CHECK"
        
        print(f"{check_text} - {t('update_checking')}")
        
        # URL для получения последнего релиза
        url = "https://api.github.com/repos/MoTyaZ1/WarTunder-DiscordRichPresence/releases/latest"
        
        # Делаем запрос к GitHub API
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            release_data = response.json()
            latest_version = release_data.get("tag_name", "")
            html_url = release_data.get("html_url", "")
            
            # Получаем текущую версию
            current_version = "v1.3.0"  # Версия по умолчанию
            
            # Пробуем прочитать версию из файла version.txt если он есть
            version_file = os.path.join(BASE_PATH, "version.txt")
            if os.path.exists(version_file):
                try:
                    with open(version_file, "r", encoding="utf-8") as f:
                        current_version = f.read().strip()
                except:
                    pass
            
            # Сравниваем версии
            if latest_version and latest_version != current_version:
                print(f"{update_text} - {t('update_current_version')}: {current_version}")
                print(f"{update_text} - {t('update_latest_version')}: {latest_version}")
                print(f"{update_text} - {t('update_download')}: {html_url}")
            else:
                # Выводим текущую версию
                print(f"{update_text} - {t('update_current_version')}: {current_version}")
            
    except requests.exceptions.ConnectionError:
        # Если нет интернета
        print(f"{update_text} - {t('update_no_internet')}")
        return False
    except requests.exceptions.RequestException as e:
        # Если GitHub недоступен
        print(f"{update_text} - {t('update_check_failed')}")
        return False
    except Exception as e:
        # Любая другая ошибка
        print(f"{update_text} - {t('update_check_failed')}")
        return False

def main():
    """Основная функция"""
    try:
        # Сначала загружаем язык из settings.json
        language = load_language_from_settings()
        set_language(language)
        
        # Получаем функции перевода и цветов
        t = get_translation_func(language)
        colored_text = get_colored_text_func()
        
        # Создаем цветные префиксы
        success_text = colored_text("SUCCESS", "SUCCESS")
        error_text = colored_text("ERROR", "ERROR")
        info_text = colored_text("INFO", "INFO")
        warning_text = colored_text("WARNING", "WARNING")
        
        # Проверка обновлений в самом начале
        check_for_updates(language)
        
        # Проверка файлов
        settings_path = os.path.join(BASE_PATH, "settings.json")
        if not os.path.exists(settings_path):
            print(f"{info_text} - Creating settings.json...")
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
                print(f"{success_text} - settings.json created")
            except Exception as e:
                print(f"{error_text} - Error loading settings.json: {e}")
                input(f"\n{t('press_enter')}")
                return
        else:
            print(f"{success_text} - settings.json")
        
        # Пытаемся импортировать остальные модули
        try:
            # Для EXE режима импортируем напрямую
            if getattr(sys, 'frozen', False):
                try:
                    from configs import settings
                    from configs import logs
                    from game import api as game_api
                    from discord import handler
                    
                    # Пробуем разные варианты для discord rpc
                    try:
                        from discord import rpc as discord_init
                    except ImportError:
                        from discord import init as discord_init
                    
                    print(f"{info_text} - Modules imported successfully in EXE mode")
                    
                except ImportError as e:
                    print(f"{error_text} - Failed to import modules in EXE mode: {e}")
                    raise ImportError("Failed to import modules")
            else:
                # Для обычного режима используем load_module
                settings = load_module("settings", os.path.join(BASE_PATH, "configs", "settings.py"))
                logs = load_module("logs", os.path.join(BASE_PATH, "configs", "logs.py"))
                game_api = load_module("game_api", os.path.join(BASE_PATH, "game", "api.py"))
                handler = load_module("handler", os.path.join(BASE_PATH, "discord", "handler.py"))
                
                # Пробуем загрузить rpc.py или init.py
                rpc_path = os.path.join(BASE_PATH, "discord", "rpc.py")
                if not os.path.exists(rpc_path):
                    rpc_path = os.path.join(BASE_PATH, "discord", "init.py")
                
                discord_init = load_module("discord_init", rpc_path)
            
            # Проверяем что все модули загружены
            if not all([settings, logs, game_api, handler, discord_init]):
                print(f"{error_text} - Failed to load required modules:")
                if not settings: print("  - settings.py")
                if not logs: print("  - logs.py")
                if not game_api: print("  - game/api.py")
                if not handler: print("  - discord/handler.py")
                if not discord_init: print("  - discord/rpc.py or discord/init.py")
                raise ImportError("Failed to load required modules")
            
        except Exception as e:
            print(f"\n{error_text} - Error importing modules: {e}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
            sys.exit(1)
        
        # Инициализация настроек
        try:
            app_settings = settings.init_presence_settings(BASE_PATH)
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
        print(f"\n{info_text} - {t('program_started')}")
        
        # Предупреждение - 16 попыток по 10 секунд
        print(f"\n{warning_text} - {t('program_will_try')}")
        
        # Запуск основного цикла
        try:
            handler.run_update_presence_loop(app_settings, http_client)
        except KeyboardInterrupt:
            print(f"\n\n{info_text} - Program stopped by user")
        except Exception as e:
            critical_error = colored_text("CRITICAL ERROR", "CRITICAL ERROR")
            print(f"\n\n{critical_error} - {e}")
            traceback.print_exc()
            input(f"\n{t('press_enter')}")
        
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print(f"\n\n{info_text} - Program stopped by user")
    except Exception as e:
        critical_error = colored_text("CRITICAL ERROR", "CRITICAL ERROR")
        print(f"\n\n{critical_error} - {e}")
        traceback.print_exc()
        input(f"\nPress Enter to exit...")

if __name__ == "__main__":
    main()