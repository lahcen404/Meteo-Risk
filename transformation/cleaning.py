import pandas as pd
import os

class DataCleaner:
    
    
    def clean_weather(self,data):
        data = data.copy()
        
        data.columns = data.columns.str.strip() # remove spaces
        
        data["forecast_date"] = pd.to_datetime(data["forecast_date"])
        
        numeric_columns = [
        "latitude",
        "longitude",
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
        "wind_speed_10m_max"
        ]
        
        for cl in numeric_columns:
            data[cl] = pd.to_numeric(data[cl],errors="coerce")


        data = data.drop_duplicates()
        
        data = data[
            data["latitude"].between(-90,90) 
            & data["longitude"].between(-180,180)
        ]
        
        data = data[data["precipitation_sum"] >= 0]

        data = data[data["wind_speed_10m_max"] >= 0]

        data = data[
            data["temperature_min"] <= data["temperature_max"]
        ]
        
        
        data = data.reset_index(drop=True)

        return data
    
    def save_to_silver(self,data):
        
        os.makedirs("data/silver",exist_ok=True)
        out_path = "data/silver/weather.csv"
        data.to_csv(out_path,index=False)
        