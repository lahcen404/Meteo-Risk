import json
import os
import pandas as pd
import requests


class WeatherExtractor:
    
    def __init__(self,url,timeout=10):
        
        self.url=url
        self.timeout = timeout
        
    def extractor(self):
        
        cities = pd.read_csv("ma.csv")
        
        all_weather = []
        
        for _,city in cities.iterrows():
            
            city_name = city["city"]
            city_longitude = city["lng"]
            city_latitude = city["lat"]
            
            params ={
                        "latitude": city_latitude,
                        "longitude": city_longitude,
                        "daily": [
                            "temperature_2m_max",
                            "temperature_2m_min",
                            "precipitation_sum",
                            "wind_speed_10m_max"
                        ]
                    }
            try:    
                dataAPI = requests.get(self.url,params=params,timeout=self.timeout)
                
                dataAPI.raise_for_status()
                data_json = dataAPI.json()
                
                
                required_fields = [
                    "time",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "wind_speed_10m_max"
                ]
                
                
                if "daily" not in data_json:
                    print(f"Invalid api response for {city_name}")
                    continue 
                
                missing_field = False

                for field in required_fields:

                    if field not in data_json["daily"]:
                        missing_field = True

                if missing_field:
                    print(f"Missing weather data for {city_name}")
                    continue
                
                
                
            except requests.Timeout:
                print(f"Timeout for {city_name}")
                continue
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {city_name}: {e}")
                continue
            
                
            city_weather = {
                        "city":city_name,
                        "lat":city_latitude,
                        "lng":city_longitude,
                        "weather":data_json
                    }
            
            all_weather.append(city_weather)
            
        return all_weather
    

    def save_raw_data(self, data):
        os.makedirs("data/bronze", exist_ok=True)

        with open("data/bronze/weather_raw.json", "w") as file:
            json.dump(data, file, indent=4)
        
        
        
        
    def parse_data_raw(self,data):
    
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
        
    
    


#with open("raw_data.json","r") as file:
 #   data = json.load(file)
    
url = "https://api.open-meteo.com/v1/forecast"


extractor = WeatherExtractor(url)

weather_raw =extractor.extractor()

#extractor.save_raw_data(weather_raw)
#print(weather_raw)
weather_df = extractor.parse_data_raw(weather_raw)
# extractor.save_to_bronze(weather_df)
print(weather_df.head())
print(weather_df.dtypes)
print(weather_df.isnull().sum())

