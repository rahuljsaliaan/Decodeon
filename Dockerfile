# Use official Python image
FROM python:3.13-rc-slim

# Set the working directory
WORKDIR /app

# Install curl and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first
COPY pyproject.toml poetry.lock* /app/

# Copy the rest of the app
COPY . /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && poetry cache clear pypi --all --no-interaction

# Expose the app port
EXPOSE 8000

# Command to run your app
CMD ["poetry", "run", "start"]

