# Use an official Python runtime as a parent image, matching your project's Python version
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the necessary project files into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install the project dependencies using Poetry
# The `--no-dev` flag avoids installing packages in the [tool.poetry.dev-dependencies] section
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the rest of your project into the container
COPY streamlit_app/ ./streamlit_app/

# Volume configuration for persistent storage
# Note: You'll need to mount the volume when running the container
VOLUME ["/usr/src/app/us-funds-project.db"]

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "./streamlit_app/etf_app.py"]
