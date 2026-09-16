import pandas as pd

class FeatureEngineer:
    def __init__(self):
        pass
    
    def temperature_category(self,temp):
        
        if temp < 5 :
            return "Very cold"
        elif temp < 15:
            return "Cold"
        elif temp < 30:
            return "Normal"
        elif temp < 40 :
            return "Hot"
        else :
            return "Very Hot"
        
        
    def precipitation_category(self, precipitation):
        if precipitation == 0:
            return "No Rain"
        elif precipitation < 5:
            return "Light"
        elif precipitation < 20:
            return "Moderate"
        elif precipitation < 50:
            return "Heavy"
        else:
            return "Extreme"
        
        
    def wind_category(self, wind_speed):
        if wind_speed < 20:
            return "Low"
        elif wind_speed < 40:
            return "Moderate"
        elif wind_speed < 60:
            return "Strong"
        else:
            return "Extreme"
        
    