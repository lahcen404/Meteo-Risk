import pandas as pd

class FeatureEngineer:
    def __init__(self):
        pass
    
        
    
    def create_features(self, data):

        data = data.copy()

        data["temperature_category"] = data["temperature_max"].apply(
            lambda temp:
                "Very cold" if temp < 5
                else "Cold" if temp < 15
                else "Normal" if temp < 30
                else "Hot" if temp < 40
                else "Very Hot"
        )

        data["precipitation_category"] = data["precipitation_sum"].apply(
            lambda precipitation:
                "No Rain" if precipitation == 0
                else "Light" if precipitation < 5
                else "Moderate" if precipitation < 20
                else "Heavy" if precipitation < 50
                else "Extreme"
        )

        data["wind_category"] = data["wind_speed_10m_max"].apply(
            lambda wind_speed:
                "Low" if wind_speed < 20
                else "Moderate" if wind_speed < 40
                else "Strong" if wind_speed < 60
                else "Extreme"
        )

        return data
        
        