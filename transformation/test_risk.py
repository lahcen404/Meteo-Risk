import pandas as pd
from risk_score import RiskCalculator


weather = pd.read_csv("data/silver/weather.csv")

calculator = RiskCalculator()

result = calculator.calculate_score(weather)

#print(result.head())
print(result[
    [
        "city",
        "forecast_date",
        "temperature_max",
        "precipitation_sum",
        "wind_speed_10m_max",
        "temperature_risk",
        "precipitation_risk",
        "wind_risk",
        "risk_score",
        "risk_level"
    ]
].head(15))