import os
import pandas as pd

from feature_engineering import FeatureEngineer
from risk_score import RiskCalculator


weather = pd.read_csv("data/silver/weather.csv")

features_enginer = FeatureEngineer()

features = features_enginer.create_features(weather)

risk_calculator = RiskCalculator()

gold = risk_calculator.calculate_score(features)


os.makedirs("data/gold", exist_ok=True)



gold.to_csv(
    "data/gold/weather_risk.csv",
    index=False
)

