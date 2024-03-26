# US-funds-performance
![etf_appStreamlit-GoogleChrome2024-03-2609-43-39-ezgif com-video-to-gif-converter](https://github.com/ctcoutinho/us-funds-performance/assets/159946582/7f8cc3a3-8cbd-4a45-a984-c6ebc8320303)

Application accessible here : https://us-funds-ctcoutinho.sbbdata.com/

Welcome to the US-Funds Dashboard, a Streamlit application designed to provide insightful and comprehensive ETF information. The app leverages the power of financial data from Yahoo Finance, processed and stored in DuckDB, and modeled using dbt following the Ralph Kimball methodology. This approach ensures that the data is not only accurate but also presented in a user-friendly and accessible manner.

## Features
- Comprehensive Analysis: Explore ETF data through various dimensions such as time, geography, and sector.
- Interactive Interface: Utilize Streamlit’s interactive features to filter and manipulate ETF data for personalized analysis.
- Data Integrity: Benefit from a rigorous data pipeline that cleans, transforms, and models the data to ensure high-quality insights.

## Getting Started

### Requirements

To run this project locally you'll need:
- python 3.10 or later
- Duckdb database file (us-funds-project.db) from S3 : [s3://us-funds-project-duck-db-bucket/us-funds-project.db](https://us-funds-project-duck-db-bucket.s3.eu-west-3.amazonaws.com/us-funds-project.db)

In order to stick with the standard way of managing python projects, [poetry](https://python-poetry.org/) will be used as package manager.

### Installation
First install poetry : 
```bash
pip install poetry
```

After having pull the project, you can install all the required dependencies for this project by running.

```bash
poetry install
```

## Running the project

For dbt and Streamlit to work, you have to place .duckdb database file at the root of the project: us-funds-performance/us-funds-project.db !

To run dbt and modify and project :

Navigate to /us_funds_dbt and run any dbt command.

To run Streamlit locally: 

Navigate to /streamlit_app and run :

```bash
streamlit run etf_app.py
```

You can now access the app on : http://localhost:8501

## Running the project using the Dockerfile

- 1) Build the Docker image from the directory containing the Dockerfile:

```bash
docker build -t us-funds-project .
```

- 2) Run the container with a mounted volume for persistent storage of your database file. This command mounts the us-funds-performance/ directory from your host to the container. 

```bash
docker run -d -p 8501:8501 -v $(pwd)/us-funds-project.db:/usr/src/app/us-funds-project.db us-funds-project
```

You can now access the app on : http://localhost:8501
