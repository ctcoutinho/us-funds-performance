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

For dbt and Streamlit to work, you have to place duckdb file at the root of the project: us-funds-performance/us-funds-project.db !

To run dbt and modify and project :

Navigate to /us_funds_dbt and run any dbt command.

To run Streamlit locally: 

Navigate to /streamlit_app and run :

```bash
streamlit run etf_app.py
```

You can now access the app on : http://localhost:8501
