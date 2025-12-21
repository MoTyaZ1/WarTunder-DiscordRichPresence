# discord/types/air.py
from dataclasses import dataclass
from configs.settings import PresenceSettings
from discord.common import VEHICLE_AIR_DICT, VEHICLE_STATES_DICT, BASIC_STATE_DICT
import json
import re

@dataclass
class IndicatorsAirStruct:
    """Structure for air vehicle indicators"""
    readable_vehicle_name: str = ""
    vehicle_code_name: str = ""  # ← Добавим поле для кодового имени
    altitude: str = ""
    tas_speed: str = ""
    ias_speed: str = ""
    current_fuel: str = ""
    max_fuel: str = ""
    
    img: str = ""
    details: str = ""
    state: str = ""
    big_text: str = ""
    
    def set_vehicle_img(self, vehicle_game_name: str):
        """Set vehicle image"""
        self.img = f"https://static.encyclopedia.warthunder.com/images/{vehicle_game_name}.png"
    
    def set_air_vehicle_name(self, vehicle_game_name: str, settings: PresenceSettings):
        """Set readable air vehicle name"""
        self.vehicle_code_name = vehicle_game_name  # ← Сохраняем кодовое имя
        
        readable_name = VEHICLE_AIR_DICT.get(vehicle_game_name, {}).get(settings.lang, "")
        
        if not readable_name:
            # Use base name
            stripped_name = vehicle_game_name.replace("_", " ")
            self.readable_vehicle_name = stripped_name
        else:
            self.readable_vehicle_name = readable_name
        
        self.set_vehicle_img(vehicle_game_name)
    
    def build_air_info(self, body_text: str) -> bool:
        """Parse air vehicle information from WT API"""
        try:
            # Reset values
            self.altitude = ""
            self.tas_speed = ""
            self.ias_speed = ""
            self.current_fuel = ""
            self.max_fuel = ""
            
            # Try to parse as JSON
            try:
                data = json.loads(body_text)
                
                # Extract data from JSON
                if "H, m" in data:
                    altitude_value = data["H, m"]
                    if altitude_value is not None:
                        self.altitude = str(int(altitude_value))
                
                if "TAS, km/h" in data:
                    tas_value = data["TAS, km/h"]
                    if tas_value is not None:
                        self.tas_speed = str(int(tas_value))
                
                if "IAS, km/h" in data:
                    ias_value = data["IAS, km/h"]
                    if ias_value is not None:
                        self.ias_speed = str(int(ias_value))
                
                if "Mfuel, kg" in data:
                    current_fuel_value = data["Mfuel, kg"]
                    if current_fuel_value is not None:
                        self.current_fuel = str(int(current_fuel_value))
                
                if "Mfuel0, kg" in data:
                    max_fuel_value = data["Mfuel0, kg"]
                    if max_fuel_value is not None:
                        self.max_fuel = str(int(max_fuel_value))
                
                # Check if we got any values
                if any([self.altitude, self.tas_speed, self.ias_speed, self.current_fuel, self.max_fuel]):
                    return True
                    
            except json.JSONDecodeError:
                # Fallback: text parsing
                if not self._parse_text_fallback(body_text):
                    return False
                return True
            
            return True
                
        except Exception as e:
            return False
    
    def _parse_text_fallback(self, body_text: str) -> bool:
        """Fallback text parsing"""
        found_values = []
        
        # Regular expressions for search
        patterns = [
            (r'"H,\s*m"\s*:\s*([0-9]+\.?[0-9]*)', 'altitude'),
            (r'H,\s*m:\s*([0-9]+\.?[0-9]*)', 'altitude_fallback'),
            (r'"TAS,\s*km/h"\s*:\s*([0-9]+\.?[0-9]*)', 'tas'),
            (r'TAS,\s*km/h:\s*([0-9]+\.?[0-9]*)', 'tas_fallback'),
            (r'"IAS,\s*km/h"\s*:\s*([0-9]+\.?[0-9]*)', 'ias'),
            (r'IAS,\s*km/h:\s*([0-9]+\.?[0-9]*)', 'ias_fallback'),
            (r'"Mfuel,\s*kg"\s*:\s*([0-9]+\.?[0-9]*)', 'current_fuel'),
            (r'Mfuel,\s*kg:\s*([0-9]+\.?[0-9]*)', 'current_fuel_fallback'),
            (r'"Mfuel0,\s*kg"\s*:\s*([0-9]+\.?[0-9]*)', 'max_fuel'),
            (r'Mfuel0,\s*kg:\s*([0-9]+\.?[0-9]*)', 'max_fuel_fallback'),
        ]
        
        for pattern, param_name in patterns:
            matches = re.findall(pattern, body_text)
            if matches:
                value = matches[0]
                cleaned_value = str(int(float(value))) if '.' in str(value) else str(value)
                
                if 'altitude' in param_name and not self.altitude:
                    self.altitude = cleaned_value
                    found_values.append('altitude')
                elif 'tas' in param_name and not self.tas_speed:
                    self.tas_speed = cleaned_value
                    found_values.append('tas')
                elif 'ias' in param_name and not self.ias_speed:
                    self.ias_speed = cleaned_value
                    found_values.append('ias')
                elif 'current_fuel' in param_name and not self.current_fuel:
                    self.current_fuel = cleaned_value
                    found_values.append('current_fuel')
                elif 'max_fuel' in param_name and not self.max_fuel:
                    self.max_fuel = cleaned_value
                    found_values.append('max_fuel')
        
        return len(found_values) > 0
    
    def set_big_img_text(self, settings: PresenceSettings):
        """Set large image text"""
        if settings.alt_presence:
            left_text = ""
            right_text = ""
            
            # Left parameter
            if settings.left_air_state == "spd" and self.tas_speed:
                left_text = f"{VEHICLE_STATES_DICT['speed_tas'][settings.lang]}: {self.tas_speed} km/h"
            elif settings.left_air_state == "ias" and self.ias_speed:
                left_text = f"{VEHICLE_STATES_DICT['ias'][settings.lang]}: {self.ias_speed} km/h"
            
            # Right parameter
            if settings.right_air_state == "alt" and self.altitude:
                right_text = f"{VEHICLE_STATES_DICT['altitude'][settings.lang]}: {self.altitude} m"
            elif settings.right_air_state == "fuel" and self.current_fuel and self.max_fuel:
                right_text = f"{VEHICLE_STATES_DICT['fuel'][settings.lang]}: {self.current_fuel}/{self.max_fuel} kg"
            
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
    
    def set_state(self, settings: PresenceSettings):
        """Set state"""
        if not settings.alt_presence:
            # When alt_presence is off, show info in state
            left_text = ""
            right_text = ""
            
            # Left parameter
            if settings.left_air_state == "spd" and self.tas_speed:
                left_text = f"{VEHICLE_STATES_DICT['speed_tas'][settings.lang]}: {self.tas_speed} km/h"
            elif settings.left_air_state == "ias" and self.ias_speed:
                left_text = f"{VEHICLE_STATES_DICT['ias'][settings.lang]}: {self.ias_speed} km/h"
            
            # Right parameter
            if settings.right_air_state == "alt" and self.altitude:
                right_text = f"{VEHICLE_STATES_DICT['altitude'][settings.lang]}: {self.altitude} m"
            elif settings.right_air_state == "fuel" and self.current_fuel and self.max_fuel:
                right_text = f"{VEHICLE_STATES_DICT['fuel'][settings.lang]}: {self.current_fuel}/{self.max_fuel} kg"
            
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
    
    def set_details(self, settings: PresenceSettings):
        """Set details"""
        if settings.vehicle_details:
            self.details = f"{VEHICLE_STATES_DICT['play_on'][settings.lang]}: {self.readable_vehicle_name}"
        else:
            self.details = ""