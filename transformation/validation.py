import pandas as pd

class DataValidator:
    
    def validate_cities(self, data):
        
        required_columns = ["city", "latitude", "longitude"]
        
        return all(
                    column in data.columns
                    for column in required_columns)
        
    def validate_weather(self,data):
        
        required_columns = [
            "forecast_date",
            "temperature_max",
            "temperature_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ]
        
        return all(
            column in data.columns
            for column in required_columns
        )
        
        
    def check_validate_values(self,data):
        
        checks = {
            
            "missing_values": data.isnull().sum().sum() == 0,
            "duplicates": data.duplicated().sum() == 0,
            "valid_coordinates": (
                data["latitude"].between(-90, 90).all()
                and data["longitude"].between(-180, 180).all()
            ),
            "valid_precipitation": (
                data["precipitation_sum"] >= 0
            ).all(),
            "valid_wind": (
                data["wind_speed_10m_max"] >= 0
            ).all(),
            "valid_temperature": (
                data["temperature_min"]
                <= data["temperature_max"]
            ).all()
        }

        return checks