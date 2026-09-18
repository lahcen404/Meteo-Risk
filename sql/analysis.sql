-- 1. citiees  with the highest weather risk
SELECT
    c.name AS city,
    ROUND(AVG(wr.risk_score), 2) AS average_risk
FROM weather_risks wr
JOIN weather_forecasts wf
    ON wr.weather_id = wf.id
JOIN cities c
    ON wf.city_id = c.id
GROUP BY c.name
ORDER BY average_risk DESC;

-- 2. highesst risk forecast periods
SELECT
    c.name AS city,
    wf.forecast_date,
    wr.risk_score,
    wr.risk_level
FROM weather_risks wr
JOIN weather_forecasts wf
    ON wr.weather_id = wf.id
JOIN cities c
    ON wf.city_id = c.id
ORDER BY wr.risk_score DESC
LIMIT 10;

-- 3. weatheer risks for a specific city
SELECT
    c.name AS city,
    wf.forecast_date,
    wf.temperature_max,
    wf.temperature_min,
    wf.precipitation_sum,
    wf.wind_speed_max,
    wr.risk_score,
    wr.risk_level
FROM weather_forecasts wf
JOIN cities c
    ON wf.city_id = c.id
JOIN weather_risks wr
    ON wr.weather_id = wf.id
WHERE c.name = 'Casablanca'
ORDER BY wf.forecast_date;

-- 4. numberr of risky periods by risk level
SELECT
    wr.risk_level,
    COUNT(*) AS number_of_periods
FROM weather_risks wr
GROUP BY wr.risk_level
ORDER BY number_of_periods DESC;

-- 5. higheest risk for each city
SELECT
    c.name AS city,
    MAX(wr.risk_score) AS maximum_risk
FROM weather_risks wr
JOIN weather_forecasts wf
    ON wr.weather_id = wf.id
JOIN cities c
    ON wf.city_id = c.id
GROUP BY c.name
ORDER BY maximum_risk DESC;