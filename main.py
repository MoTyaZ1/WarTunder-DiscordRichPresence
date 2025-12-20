import sys
import os
import traceback

# Добавляем все подпапки в sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
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
        if os.path.exists("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
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
            spec = importlib.util.spec_from_file_location(
                "translations", 
                os.path.join(script_dir, "configs", "translations.py")
            )
            translations_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(translations_module)
            t = lambda key: translations_module.get_translation(language, key)
        except Exception as e:
            print(f"Ошибка загрузки переводов: {e}")
            t = lambda key: key
        
        # Загружаем цвета напрямую
        try:
            spec = importlib.util.spec_from_file_location(
                "colors", 
                os.path.join(script_dir, "configs", "colors.py")
            )
            colors_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(colors_module)
            colored_text = colors_module.colored_text
        except Exception as e:
            print(f"Ошибка загрузки цветов: {e}")
            def colored_text(text: str, color_name: str) -> str:
                return text
        
        check_text = colored_text("CHECK", "CHECK")
        success_text = colored_text("SUCCESS", "SUCCESS")
        error_text = colored_text("ERROR", "ERROR")
        
        # Проверка файлов
        print(f"{check_text} [1/2]")
        
        if not os.path.exists("settings.json"):
            print(f"{t('creating_file')}")
            try:
                with open("settings.json", "w", encoding="utf-8") as f:
                    f.write(f'''{{
  "refresh_time": 7,
  "large_img": "main_logo",
  "alt_presence": false,
  "lang": "{language}",
  "vehicle_details": true,
  "left_tank_state": "speed",
  "right_tank_state": "crew",
  "left_air_state": "spd",
  "right_air_state": "alt",
  "debug_mode": false
}}''')
                print(f"{success_text} {t('file_created')}")
            except Exception as e:
                print(f"{error_text} - {t('loading_error')} {e}")
                input(f"\n{t('press_enter')}")
                return
        else:
            print(f"{success_text} settings.json")
        
        # Проверка зависимостей
        print(f"\n{check_text} [2/2]")
        try:
            import pypresence
            print(f"{success_text} pypresence")
        except ImportError as e:
            print(f"{error_text} - pypresence {t('deps_not_installed')}")
            print(f"{t('install_command')} pypresence")
            sys.exit(1)
        
        try:
            import requests
            print(f"{success_text} requests")
        except ImportError as e:
            print(f"{error_text} - requests {t('deps_not_installed')}")
            print(f"{t('install_command')} requests")
            sys.exit(1)
        
        # Импортируем остальные модули напрямую
        try:
            # settings.py
            spec = importlib.util.spec_from_file_location(
                "settings", 
                os.path.join(script_dir, "configs", "settings.py")
            )
            settings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings_module)
            
            # logs.py
            spec = importlib.util.spec_from_file_location(
                "logs", 
                os.path.join(script_dir, "configs", "logs.py")
            )
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
            app_settings = settings.init_presence_settings()
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