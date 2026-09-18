import pandas as pd


def get_risk_data(engine):

    query = """
        SELECT
            c.name AS city,
            wf.forecast_date,
            wf.temperature_max,
            wf.temperature_min,
            wf.precipitation_sum,
            wf.wind_speed_max,
            wr.temperature_category,
            wr.precipitation_category,
            wr.wind_category,
            wr.risk_score,
            wr.risk_level
        FROM weather_risks wr
        JOIN weather_forecasts wf
            ON wr.weather_id = wf.id
        JOIN cities c
            ON wf.city_id = c.id
        ORDER BY wf.forecast_date;
    """

    return pd.read_sql(query, engine)