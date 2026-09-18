import pandas as pd
from validation import DataValidator


weather_df = pd.read_csv("data/silver/weather.csv")

validator = DataValidator()

print("Cities clmns:")
print(validator.validate_cities(weather_df))

print()

print("Weather clmns:")
print(validator.validate_weather(weather_df))

print()

print("Value validation:")
print(validator.check_validate_values(weather_df))

print(weather_df.columns.tolist())