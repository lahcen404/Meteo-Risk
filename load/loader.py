import pandas as pd

from database import Database

class DatabaseLoader:
    def __init__(self):
        self.database = Database()
    

    def load_cities(self,data):
        
        cities = data[["city","latitude","longitude"]].drop_duplicates()
        
        cities = cities.rename(
            columns={"city": "name"}
        )
        
        cities.to_sql(
            "cities",
            self.database.engine,
            if_exists="append",
            index=False
        )
        
        
    def load_weather(self, data):
        
        
            cities = pd.read_sql("SELECT id, name FROM cities",
                                self.database.engine)
            
            weather = data.merge(
                cities,
                left_on="city",
                right_on="name",
                how="left"
                
            )
         
            weather = weather.rename(
                columns={
                    "id":"city_id",
                    "wind_speed_10m_max": "wind_speed_max"
                }
            )
            

            weather = weather[[
                "forecast_date",
                "city_id",
                "temperature_max",
                "temperature_min",
                "precipitation_sum",
                "wind_speed_max"
            ]]

            

            weather.to_sql(
                "weather_forecasts",
                self.database.engine,
                if_exists="append",
                index=False
            )
            
    def load_risks(self, data):

        forecasts = pd.read_sql(
            """
            SELECT
                wf.id AS weather_id,
                c.name AS city,
                wf.forecast_date
            FROM weather_forecasts wf
            JOIN cities c
                ON c.id = wf.city_id
            """,
            self.database.engine
        )

        # check datttes same type
        data["forecast_date"] = pd.to_datetime(
            data["forecast_date"]
        ).dt.date

        forecasts["forecast_date"] = pd.to_datetime(
            forecasts["forecast_date"]
        ).dt.date

        risks = data.merge(
            forecasts,
            on=["city", "forecast_date"],
            how="left"
        )

        # cheeeck if some weather records were not found
        missing = risks["weather_id"].isna().sum()

        if missing > 0:
            print("risks have no matching weather forecast")
            print(
                risks[risks["weather_id"].isna()][
                    ["city", "forecast_date"]
                ].head()
            )

        risks = risks[[
            "weather_id",
            "temperature_category",
            "precipitation_category",
            "wind_category",
            "risk_score",
            "risk_level"
        ]]

        risks.to_sql(
            "weather_risks",
            self.database.engine,
            if_exists="append",
            index=False
        )
                

data = pd.read_csv("data/gold/weather_risk.csv")

loader = DatabaseLoader()

#loader.load_cities(data)
print("Cities loaded successfully!!")
#loader.load_weather(data)
print("Weather data loaded successfully.")
loader.load_risks(data)
print("Risks loaded successs !!")
