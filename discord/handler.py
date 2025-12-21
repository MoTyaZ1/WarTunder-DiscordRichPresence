# discord/handler.py
import time
import logging
import sys

from configs.settings import PresenceSettings
from discord.common import BASIC_STATE_DICT, VEHICLE_STATES_DICT
from discord.types.map import MapStruct
from discord.types.info import MainInfoStruct
from game import api as game_api
from configs import logs as tools_logger
from discord.init import get_rpc_client, get_start_time

# Импортируем функции для цветов и переводов
try:
    from configs.colors import colored_text
    from configs.translations import get_translation
except ImportError as e:
    # Fallback функции на случай ошибки импорта
    def colored_text(text: str, color_name: str) -> str:
        return text
    
    def get_translation(lang: str, key: str) -> str:
        return key

logger = logging.getLogger(__name__)

def set_presence(state: str, details: str, large_img: str, large_text: str, 
                small_img: str = "", small_text: str = "", lang: str = "en") -> bool:
    """Set Discord status"""
    try:
        rpc = get_rpc_client()
        start_time = get_start_time()
        
        # Make sure all required fields are filled
        if not state:
            state = VEHICLE_STATES_DICT["in_game"]["ru"]
        if not details:
            details = ""  # Пустая строка вместо "War Thunder"
        if not large_img:
            large_img = "main_logo"
        if not large_text:
            large_text = "War Thunder"
        
        # Используем новый метод set_activity
        rpc.set_activity(
            state=state,
            details=details if details else None,
            large_image=large_img,
            large_text=large_text,
            small_image=small_img if small_img else None,
            small_text=small_text if small_text else None,
            start=start_time
        )
        
        # Получаем перевод для "Статус обновлен"
        status_updated_text = get_translation(lang, "discord_status_updated")
        
        # Выводим напрямую в консоль
        discord_text = colored_text("DISCORD", "DISCORD")
        print(f"{discord_text} - {status_updated_text}: {state}")
        return True
        
    except Exception as e:
        tools_logger.error_log_presence_struct(e, state, details, large_img, large_text, small_img, small_text)
        logger.error(f"Error setting status: {e}")
        return False

def set_ground_state(settings: PresenceSettings, main_info: MainInfoStruct) -> bool:
    """Set status for ground vehicles"""
    try:
        from discord.types.ground import IndicatorsGroundStruct
        ground_indicators = IndicatorsGroundStruct()
        ground_indicators.set_ground_vehicle_name(main_info.vehicle_game_name, settings)
        ground_indicators.set_speed_crew_data(
            main_info.speed, 
            main_info.crew_total, 
            main_info.crew_current,
            main_info.rpm
        )
        ground_indicators.set_big_img_text(settings)
        ground_indicators.set_state(settings)
        ground_indicators.set_details(settings)
        
        return set_presence(
            state=ground_indicators.state,
            details=ground_indicators.details,
            large_img=ground_indicators.img if ground_indicators.img else settings.large_img,
            large_text=ground_indicators.big_text,
            small_img=settings.large_img,
            small_text="War Thunder",
            lang=settings.lang
        )
    except Exception as e:
        logger.error(f"Error setting ground vehicle status: {e}", exc_info=True)
        return False

def set_air_state(settings: PresenceSettings, http_client, main_info: MainInfoStruct) -> bool:
    """Set status for air vehicles"""
    try:
        if settings.debug_mode:
            print(f"[DEBUG] Air vehicle code from API: {main_info.vehicle_game_name}")
        
        success, state_body = game_api.air_state_request(http_client, settings.debug_mode, settings.lang)
        
        if not success:
            logger.error("Failed to get data from WT API")
            return False
        
        if not state_body:
            logger.error("Empty response body from WT API")
            return False
        
        from discord.types.air import IndicatorsAirStruct
        air_indicators = IndicatorsAirStruct()
        
        if not air_indicators.build_air_info(state_body):
            logger.warning("Failed to parse air vehicle information")
            air_indicators.set_air_vehicle_name(main_info.vehicle_game_name, settings)
            air_indicators.set_details(settings)
            air_indicators.state = BASIC_STATE_DICT["in_battle"][settings.lang]
            air_indicators.big_text = air_indicators.readable_vehicle_name
            
            return set_presence(
                state=air_indicators.state,
                details=air_indicators.details,
                large_img=air_indicators.img if air_indicators.img else settings.large_img,
                large_text=air_indicators.big_text,
                small_img=settings.large_img,
                small_text="War Thunder",
                lang=settings.lang
            )
        
        air_indicators.set_air_vehicle_name(main_info.vehicle_game_name, settings)
        air_indicators.set_big_img_text(settings)
        air_indicators.set_state(settings)
        air_indicators.set_details(settings)
        
        return set_presence(
            state=air_indicators.state,
            details=air_indicators.details,
            large_img=air_indicators.img if air_indicators.img else settings.large_img,
            large_text=air_indicators.big_text,
            small_img=settings.large_img,
            small_text="War Thunder",
            lang=settings.lang
        )
    except Exception as e:
        logger.error(f"Error setting air vehicle status: {e}", exc_info=True)
        return False

def run_update_presence_loop(settings: PresenceSettings, http_client):
    """Main status update loop"""
    # Создаем функцию перевода один раз
    t = lambda key: get_translation(settings.lang, key)
    
    # Выводим сообщение о начале цикла с переводом
    try:
        from configs.colors import colored_text
        info_text = colored_text("INFO", "INFO")
        message = t('starting_update_loop').format(interval=settings.refresh_time)
        print(f"{info_text} - {message}")
    except:
        print(f"INFO - Starting status update loop (interval: {settings.refresh_time}s)")
    
    next_update_time = time.time()
    max_iterations = 10000  # Защита от бесконечного цикла
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        try:
            current_time = time.time()
            
            if current_time < next_update_time:
                sleep_time = next_update_time - current_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            next_update_time = time.time() + settings.refresh_time
            
            if game_api.check_connection_failed():
                # Используем CRITICAL ERROR вместо CRITICAL
                try:
                    from configs.colors import colored_text
                    critical_error = colored_text("CRITICAL ERROR", "CRITICAL ERROR")
                    print(f"\n{critical_error} - {t('wt_not_running')}")
                except:
                    print(f"\nCRITICAL ERROR - {t('wt_not_running')}")
                
                # Даем время на корректное завершение
                time.sleep(0.5)
                
                # Закрываем Discord соединение перед выходом
                try:
                    from discord.init import close_rpc
                    close_rpc()
                except:
                    pass
                
                # Даем еще немного времени
                time.sleep(0.3)
                
                sys.exit(1)
            
            map_data = game_api.map_request(http_client, settings.debug_mode, settings.lang)
            
            if not map_data.game_running:
                # Game not running
                set_presence(
                    state=BASIC_STATE_DICT["launching"][settings.lang],
                    details="",
                    large_img=settings.large_img,
                    large_text="War Thunder",
                    lang=settings.lang
                )
                
            elif map_data.valid:
                # Game running and in battle
                indicators = game_api.main_info_request(http_client, settings.debug_mode, settings.lang)
                if not indicators:
                    set_presence(
                        state=BASIC_STATE_DICT["in_battle"][settings.lang],
                        details="",
                        large_img=settings.large_img,
                        large_text="War Thunder",
                        lang=settings.lang
                    )
                    continue
                
                if indicators.army_type == "dummy_plane" or indicators.vehicle_game_name == "dummy_plane":
                    set_presence(
                        state=BASIC_STATE_DICT["loading"][settings.lang],
                        details="",
                        large_img=settings.large_img,
                        large_text="War Thunder",
                        lang=settings.lang
                    )
                    
                elif indicators.army_type == "air":
                    set_air_state(settings, http_client, indicators)
                    
                elif indicators.army_type == "tank":
                    set_ground_state(settings, indicators)
                    
                else:
                    set_presence(
                        state=VEHICLE_STATES_DICT["in_game"][settings.lang],
                        details="",
                        large_img=settings.large_img,
                        large_text="War Thunder",
                        lang=settings.lang
                    )
                    
            else:
                # Game running but not in battle (in hangar)
                set_presence(
                    state=BASIC_STATE_DICT["hangar"][settings.lang],
                    details="",
                    large_img=settings.large_img,
                    large_text="War Thunder",
                    lang=settings.lang
                )
                
        except SystemExit:
            # Даем время на корректное завершение
            try:
                from discord.init import close_rpc
                close_rpc()
            except:
                pass
            time.sleep(0.3)
            raise
            
        except KeyboardInterrupt:
            print("\n\nProgram stopped by user")
            try:
                from discord.init import close_rpc
                close_rpc()
            except:
                pass
            time.sleep(0.3)
            sys.exit(0)
            
        except Exception as e:
            # Используем error вместо critical для ошибок в цикле
            logger.error(f"Error in update loop (iteration {iteration}): {e}", exc_info=True)
            set_presence(
                state=BASIC_STATE_DICT["launching"][settings.lang],
                details="",
                large_img=settings.large_img,
                large_text="War Thunder",
                lang=settings.lang
            )
    
    # Если достигнуто максимальное количество итераций
    try:
        from configs.colors import colored_text
        error_text = colored_text("ERROR", "ERROR")
        print(f"\n{error_text} - Max iterations ({max_iterations}) reached, exiting loop")
    except:
        print(f"\nERROR - Max iterations ({max_iterations}) reached, exiting loop")
    
    sys.exit(1)