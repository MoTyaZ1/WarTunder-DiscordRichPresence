# configs/translations.py
TRANSLATIONS = {
    "ru": {
        # Main messages
        "download_new_version": "Скачайте новую версию:",
        "checking_dependencies": "[2/3] Проверка зависимостей...",
        "checking_files": "[3/3] Проверка наличия settings.json....",
        "file_not_found": "Файл settings.json не найден, используются настройки по умолчанию",
        "press_enter": "Нажмите Enter для выхода...",
        "program_started": "программа запущена",
        "program_will_try": "Программа будет пытаться подключиться к War Thunder 16 раз с задержкой 10 секунд между попытками. Если игра не запущена - программа завершится.",
        
        # Discord messages
        "discord_connecting": "Подключение попытка #",
        "discord_connected": "Успешно подключено",
        "discord_not_found": "Discord не найден",
        "discord_waiting": "ожидание",
        "discord_seconds": "секунд...",
        "discord_invalid_id": "Неверный ID приложения",
        "discord_image_problem": "Проблема с изображением, пробуем другой вариант...",
        "discord_alt_success": "Подключение успешно с альтернативным изображением",
        "discord_retry_failed": "Повторная попытка не удалась",
        "discord_connection_error": "Ошибка подключения",
        "discord_failed_attempts": "Не удалось подключиться к Discord после",
        "discord_attempts": "попыток",
        "discord_status_updated": "Статус обновлен",
        "app_id": "ID приложения",
        
        # API messages
        "api_unavailable": "War Thunder API недоступен",
        "attempt": "Попытка",
        "waiting": "ожидание",
        "max_attempts": "Максимальное количество попыток подключения к War Thunder достигнуто",
        "wt_not_running": "War Thunder не запущен или нет подключения к War Thunder API",
        "connection_error": "Ошибка подключения",
        "starting_update_loop": "Начало цикла обновления статуса (интервал: {interval}s)",
        "attempt_waiting": "Попытка #{attempt}: ожидание {seconds} секунд...",
        "max_attempts_reached": "Достигнуто максимальное количество попыток подключения к War Thunder",
        
        # Handler debug messages\
        "error_api_data": "Не удалось получить данных от API WT",
        "error_api_empty": "Пустое тело ответа от API WT",
        
        # Logger messages
        "logger_initialized": "Логгер инициализирован",
        
        # Update messages
        "update_checking": "Проверка обновлений...",
        "update_current_version": "Текущая версия",
        "update_latest_version": "Доступная версия",
        "update_download": "Скачать",
        "update_no_internet": "Нет подключения к интернету для проверки обновлений",
        "update_check_failed": "Не удалось проверить обновления",
    },
    "en": {
        # Main messages
        "download_new_version": "Download new version:",
        "checking_dependencies": "[2/3] Checking dependencies...",
        "checking_files": "[3/3] Checking for settings.json....",
        "file_not_found": "settings.json file not found, using default settings",
        "press_enter": "Press Enter to exit...",
        "program_started": "program started",
        "program_will_try": "The program will try to connect to War Thunder 16 times with 10 seconds delay between attempts. If the game is not running - the program will exit.",
        
        # Discord messages
        "discord_connecting": "Connecting attempt #",
        "discord_connected": "Successfully connected",
        "discord_not_found": "Discord not found",
        "discord_waiting": "waiting",
        "discord_seconds": "seconds...",
        "discord_invalid_id": "Invalid application ID",
        "discord_image_problem": "Image problem, trying another option...",
        "discord_alt_success": "Connection successful with alternative image",
        "discord_retry_failed": "Retry attempt failed",
        "discord_connection_error": "Connection error",
        "discord_failed_attempts": "Failed to connect to Discord after",
        "discord_attempts": "attempts",
        "discord_status_updated": "Status updated",
        "app_id": "Application ID",
        
        # API messages
        "api_unavailable": "War Thunder API unavailable",
        "attempt": "Attempt",
        "waiting": "waiting",
        "max_attempts": "Max connection attempts to War Thunder reached",
        "wt_not_running": "War Thunder not running or no connection to War Thunder API",
        "connection_error": "Connection error",
        "starting_update_loop": "Starting status update loop (interval: {interval}s)",
        "attempt_waiting": "Attempt #{attempt}: waiting {seconds} seconds...",
        "max_attempts_reached": "Max connection attempts to War Thunder reached",
        
        # Logger messages
        "logger_initialized": "Logger initialized",
        
        # Update messages
        "update_checking": "Checking for updates...",
        "update_current_version": "Current version",
        "update_latest_version": "Available version",
        "update_download": "Download",
        "update_no_internet": "No internet connection to check for updates",
        "update_check_failed": "Failed to check for updates",
    }
}

def get_translation(lang: str, key: str) -> str:
    """Get translation for specific language"""
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    # Fallback to English
    return TRANSLATIONS["en"].get(key, key)