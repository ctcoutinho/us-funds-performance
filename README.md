# US-funds-performance

## Setup

### Requirements

To run this project locally you'll need:
- python 3.10 or later
- us-funds-project.db from S3 : [s3://us-funds-project-duck-db-bucket/us-funds-project.db](https://us-funds-project-duck-db-bucket.s3.eu-west-3.amazonaws.com/us-funds-project.db)

In order to stick with the standard way of managing python projects, [poetry](https://python-poetry.org/) will be used as package manager.
See [FAQ](#faq) for common issues.

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
