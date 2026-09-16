import pandas as pd
from cleaning import DataCleaner

weather_df = pd.read_csv("data/bronze/weather.csv")

cleaner = DataCleaner()

cleaned_df = cleaner.clean_weather(weather_df)

print(cleaned_df.head())
print("----")
print("Duplicates:", cleaned_df.duplicated().sum())
print(cleaned_df.dropna())

print(cleaned_df.dtypes)
print(cleaned_df.isnull().sum())

cleaner.save_to_silver(cleaned_df)