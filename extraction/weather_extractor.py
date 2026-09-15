import json
import os
import pandas as pd
import requests


class Weather_Extractor:
    
    def __init__(self,url,timeout=10):
        
        self.url=url
        self.timeout = timeout
        
        
    def parse_data(self,data):
    
        all_weather = []

        for ct_data in data:
            
            daily= ct_data["weather"]["daily"]
            
            df = pd.DataFrame({
            
                "city":ct_data["city"],
                "forecast_date":daily["time"],
                "latitude":ct_data["lat"],
                "longitude":ct_data["lng"],
                "temperature_max":daily["temperature_2m_max"],
                "temperature_min":daily["temperature_2m_min"],
                "precipitation_sum":daily["precipitation_sum"],
                "wind_speed_10m_max":daily["wind_speed_10m_max"]
                
            })
            
            all_weather.append(df)
            
        return pd.concat(all_weather,ignore_index=True)
        
    def save_to_bronze(self,data):
        
        os.makedirs("data/bronze",exist_ok=True)
        
        out_path = "data/bronze/weather.csv"
        data.to_csv(out_path,index=False)
        
        


with open("raw_data.json","r") as file:
    data = json.load(file)
    
url = "https://api.open-meteo.com/v1/forecast"


extractor = Weather_Extractor(url)

weather_df =extractor.parse_data(data)
extractor.save_to_bronze(weather_df)
print(weather_df)
