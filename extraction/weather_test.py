import json
import pandas as pd


with open("raw_data.json","r") as file:
    data = json.load(file)
    
    
all_weather = []

for ct_data in data:
    
    
    daily= ct_data["weather"]["daily"]

    df = pd.DataFrame({
        
        "city":ct_data["city"],
        "latitude":ct_data["lat"],
        "longitude":ct_data["lng"],
        "forecast_date":daily["time"],
        "temperature_max":daily["temperature_2m_max"],
        "temperature_min":daily["temperature_2m_min"],
        "precipitation_sum":daily["precipitation_sum"],
        "wind_speed_10m_max":daily["wind_speed_10m_max"]
    }
    )

    all_weather.append(df)

#print(all_weather)

all_data = pd.concat(all_weather,ignore_index=True)

print(all_data.shape)