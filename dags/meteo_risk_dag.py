import os
import sys
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

from extraction.weather_extractor import WeatherExtractor
from load.loader import DatabaseLoader
from transformation.cleaning import DataCleaner
from transformation.feature_engineering import FeatureEngineer
from transformation.risk_score import RiskCalculator
from transformation.validation import DataValidator

BASE_DIR = PROJECT_ROOT
BRONZE_DIR = os.path.join(BASE_DIR, "data", "bronze")
SILVER_DIR = os.path.join(BASE_DIR, "data", "silver")
GOLD_DIR = os.path.join(BASE_DIR, "data", "gold")
BRONZE_PATH = os.path.join(BRONZE_DIR, "weather.csv")
SILVER_PATH = os.path.join(SILVER_DIR, "weather.csv")
GOLD_PATH = os.path.join(GOLD_DIR, "weather_risk.csv")
API_URL = "https://api.open-meteo.com/v1/forecast"


def extract_data():
    extractor = WeatherExtractor(API_URL)
    weather_raw = extractor.extractor()
    extractor.save_raw_data(weather_raw)
    weather_df = extractor.parse_data_raw(weather_raw)
    extractor.save_to_bronze(weather_df)
    print(f"Extracted {len(weather_df)} weather rows.")


def clean_transform():
    os.makedirs(SILVER_DIR, exist_ok=True)
    weather_df = pd.read_csv(BRONZE_PATH)

    cleaner = DataCleaner()
    validator = DataValidator()

    cleaned_df = cleaner.clean_weather(weather_df)

    if not validator.validate_weather(cleaned_df):
        raise ValueError("Weather validation failed after cleaning.")

    validation_results = validator.check_validate_values(cleaned_df)
    if not all(validation_results.values()):
        raise ValueError(f"Invalid weather values detected: {validation_results}")

    cleaner.save_to_silver(cleaned_df)
    print(f"Cleaned and validated {len(cleaned_df)} weather rows.")


def feature_engineering():
    os.makedirs(GOLD_DIR, exist_ok=True)
    weather_df = pd.read_csv(SILVER_PATH)

    feature_engineer = FeatureEngineer()
    risk_calculator = RiskCalculator()

    weather_df = feature_engineer.create_features(weather_df)
    weather_df = risk_calculator.calculate_score(weather_df)
    weather_df.to_csv(GOLD_PATH, index=False)
    print(f"Feature engineering and risk calculation saved to {GOLD_PATH}.")


def load_postgresql():
    gold_df = pd.read_csv(GOLD_PATH)
    loader = DatabaseLoader()
    loader.load_cities(gold_df)
    loader.load_weather(gold_df)
    loader.load_risks(gold_df)
    print("Data loaded into PostgreSQL successfully.")


def refresh_dashboard():
    print("Dashboard is ready to read the latest data from PostgreSQL.")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="meteo_risk_pipeline",
    default_args=default_args,
    description="End-to-end MeteoRisk pipeline: extraction, cleaning, feature engineering, PostgreSQL load and dashboard refresh",
    schedule="@daily",
    catchup=False,
    tags=["meteo-risk", "etl"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    clean_task = PythonOperator(
        task_id="clean_transform",
        python_callable=clean_transform,
    )

    feature_task = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
    )

    load_task = PythonOperator(
        task_id="load_postgresql",
        python_callable=load_postgresql,
    )

    dashboard_task = PythonOperator(
        task_id="refresh_dashboard",
        python_callable=refresh_dashboard,
    )

    extract_task >> clean_task >> feature_task >> load_task >> dashboard_task
