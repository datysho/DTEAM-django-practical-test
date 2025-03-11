# Use an official Python runtime as a parent image.
FROM python:3.10-slim

# Prevents Python from writing pyc files to disc and buffers stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory.
WORKDIR /app

# Install system dependencies and required packages for PostgreSQL.
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry.
RUN curl -sSL https://install.python-poetry.org | python - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only the dependency files to leverage Docker cache.
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies.
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the project.
COPY . /app/

# Expose port 8000.
EXPOSE 8000

# Run the Django development server.
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

