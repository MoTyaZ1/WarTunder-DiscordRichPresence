from dataclasses import dataclass
from configs.settings import PresenceSettings
from discord.common import VEHICLE_GROUND_DICT, VEHICLE_STATES_DICT, BASIC_STATE_DICT

@dataclass
class IndicatorsGroundStruct:
    """Structure for ground vehicle indicators"""
    readable_vehicle_name: str = ""
    vehicle_code_name: str = ""  # ← Добавим поле для кодового имени
    speed: float = 0.0
    rpm: float = 0.0
    total_crew: float = 0.0
    current_crew: float = 0.0
    
    img: str = ""
    details: str = ""
    state: str = ""
    big_text: str = ""
    debug_mode: bool = False
    
    def set_vehicle_img(self, vehicle_game_name: str):
        """Set vehicle image"""
        self.img = f"https://static.encyclopedia.warthunder.com/images/{vehicle_game_name}.png"
        
        if self.debug_mode:
            print(f"[DEBUG] Vehicle image URL: {self.img}")
    
    def set_speed_crew_data(self, speed: float, total: float, current: float, rpm: float = 0.0):
        """Set speed, crew and RPM data"""
        if self.debug_mode:
            print(f"[DEBUG] Ground vehicle data: speed={speed}, crew={current}/{total}, rpm={rpm}")
        
        self.speed = speed
        self.total_crew = total
        self.current_crew = current
        self.rpm = rpm
    
    def set_ground_vehicle_name(self, vehicle_game_name: str, settings: PresenceSettings):
        """Set readable ground vehicle name"""
        self.debug_mode = settings.debug_mode
        self.vehicle_code_name = vehicle_game_name  # ← Сохраняем кодовое имя
        
        fixed_name = vehicle_game_name.replace("tankModels/", "")
        self.set_vehicle_img(fixed_name)
        
        readable_name = VEHICLE_GROUND_DICT.get(fixed_name, {}).get(settings.lang, "")
        
        if not readable_name:
            # Use base name
            stripped_name = fixed_name.replace("_", " ")
            self.readable_vehicle_name = stripped_name
        else:
            self.readable_vehicle_name = readable_name
        
        if self.debug_mode:
            print(f"[DEBUG] Ground vehicle: {self.vehicle_code_name}")  # ← Показываем кодовое имя
            print(f"[DEBUG] Readable name: {self.readable_vehicle_name} (fixed: {fixed_name})")
    
    def set_big_img_text(self, settings: PresenceSettings):
        """Set large image text"""
        if settings.alt_presence:
            left_text = ""
            right_text = ""
            
            # Left parameter
            if settings.left_tank_state == "speed" and self.speed > 0:
                left_text = f"{VEHICLE_STATES_DICT['speed_ground'][settings.lang]}: {int(self.speed)} km/h"
            
            # Right parameter
            if settings.right_tank_state == "rpm" and self.rpm > 0:
                right_text = f"{VEHICLE_STATES_DICT['rpm'][settings.lang]}: {int(self.rpm)}"
            elif settings.right_tank_state == "crew" and self.total_crew > 0:
                right_text = f"{VEHICLE_STATES_DICT['crew_count'][settings.lang]}: {int(self.current_crew)}/{int(self.total_crew)}"
            
            # Form final text
            if left_text and right_text:
                self.big_text = f"{left_text} | {right_text}"
            elif left_text:
                self.big_text = left_text
            elif right_text:
                self.big_text = right_text
            else:
                self.big_text = BASIC_STATE_DICT["in_battle"][settings.lang]
        else:
            self.big_text = self.readable_vehicle_name
            
        if self.debug_mode:
            print(f"[DEBUG] Big text: {self.big_text}")
    
    def set_state(self, settings: PresenceSettings):
        """Set state"""
        if not settings.alt_presence:
            # When alt_presence is off, show info in state
            left_text = ""
            right_text = ""
            
            # Left parameter
            if settings.left_tank_state == "speed" and self.speed > 0:
                left_text = f"{VEHICLE_STATES_DICT['speed_ground'][settings.lang]}: {int(self.speed)} km/h"
            
            # Right parameter
            if settings.right_tank_state == "rpm" and self.rpm > 0:
                right_text = f"{VEHICLE_STATES_DICT['rpm'][settings.lang]}: {int(self.rpm)}"
            elif settings.right_tank_state == "crew" and self.total_crew > 0:
                right_text = f"{VEHICLE_STATES_DICT['crew_count'][settings.lang]}: {int(self.current_crew)}/{int(self.total_crew)}"
            
            # Form final text
            if left_text and right_text:
                self.state = f"{left_text} | {right_text}"
            elif left_text:
                self.state = left_text
            elif right_text:
                self.state = right_text
            else:
                self.state = BASIC_STATE_DICT["in_battle"][settings.lang]
        else:
            # When alt_presence is on, state is empty
            self.state = ""
            
        if self.debug_mode:
            print(f"[DEBUG] State: {self.state}")
    
    def set_details(self, settings: PresenceSettings):
        """Set details"""
        if settings.vehicle_details:
            self.details = f"{VEHICLE_STATES_DICT['play_on'][settings.lang]}: {self.readable_vehicle_name}"
        else:
            self.details = ""
            
        if self.debug_mode:
            print(f"[DEBUG] Details: {self.details}")