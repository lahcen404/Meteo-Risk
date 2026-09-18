# Meteo Risk

Meteo Risk is a weather risk analysis project that collects weather data for several cities, cleans and validates it, calculates risk indicators, and stores the results in PostgreSQL for analysis and dashboarding.

## Project purpose

The pipeline is designed to:

- extract city and weather data
- store raw bronze data
- clean and validate intermediate datasets
- engineer features and score risk levels
- load transformed data into PostgreSQL
- visualize results with Streamlit
- orchestrate tasks with Apache Airflow

## Architecture overview

The project is organized into the following main folders:

- `extraction/` — data extraction from city and weather sources
- `transformation/` — cleaning, validation, feature creation, and risk scoring
- `load/` — database connection and loading logic
- `dashboard/` — Streamlit dashboard files
- `dags/` — Airflow DAG definitions
- `data/` — bronze, silver, and gold datasets
- `sql/` — SQL schema and analysis scripts
- `config/` — project configuration
- `uml/` — diagrams

## Tech stack

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Streamlit
- Apache Airflow
- Docker / Docker Compose
- Plotly

## Project structure

```text
Meteo-Risk/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── README.md
├── raw_data.json
├── ma.csv
├── config/
│   └── settings.py
├── dags/
│   └── meteo_risk_dag.py
├── dashboard/
│   ├── app.py
│   └── queries.py
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── extraction/
│   ├── cities_extractor.py
│   ├── weather_extractor.py
│   └── weather_test.py
├── load/
│   ├── database.py
│   └── loader.py
├── sql/
│   ├── analysis.sql
│   └── schema.sql
├── transformation/
│   ├── cleaning.py
│   ├── create_gold.py
│   ├── feature_engineering.py
│   ├── risk_score.py
│   ├── test_cleaning.py
│   ├── test_risk.py
│   ├── test_validation.py
│   └── validation.py
├── uml/
│   ├── class-diagram.puml
│   └── corrected_class_uml.puml
└── tests/
```

## Environment configuration

Create a `.env` file in the project root with the required variables for PostgreSQL and pgAdmin:

```env
POSTGRES_DB=meteo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin

AIRFLOW_DB_NAME=airflow
AIRFLOW_DB_USER=airflow
AIRFLOW_DB_PASSWORD=airflow
```

## Run with Docker Compose

From the project root:

```bash
docker compose up -d
```

This starts:

- PostgreSQL on port `5432`
- pgAdmin on port `5050`
- Streamlit dashboard on port `8501`
- Airflow on port `8080`

## Run the dashboard locally

```bash
streamlit run dashboard/app.py
```

## Data flow

1. City data is extracted and saved to bronze storage.
2. Weather data is fetched from the Open-Meteo API and transformed into a DataFrame.
3. Data is cleaned and validated.
4. Features are created for weather categories.
5. Risk scores are computed.
6. Results are stored in PostgreSQL.
7. Streamlit reads the processed data for visualization.

## Notes

- The project uses a bronze/silver/gold pattern for data processing.
- Raw and intermediate datasets are stored under `data/`.
- Airflow DAGs are placed in `dags/` and can be extended for production scheduling.

## Useful links

- Streamlit dashboard: http://localhost:8501
- pgAdmin: http://localhost:5050
- Airflow: http://localhost:8080

## License

By AIT MASKOUR Lahcen