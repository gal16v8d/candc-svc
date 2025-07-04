# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3.13 -

# Install dependencies using poetry
RUN /root/.local/bin/poetry config virtualenvs.create false && \
    /root/.local/bin/poetry install --no-root --no-interaction --no-ansi

# Railway pass env to image with the following args
ARG CANDC_DB_URL
ARG POOL_RECYCLE
ARG POOL_SIZE
ARG PORT

# Expose the port in use by the app
EXPOSE ${PORT}

# Command to run your application
CMD ["gunicorn", "--workers", "2", "wsgi:app"]