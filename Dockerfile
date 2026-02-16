FROM python:3.13-slim

WORKDIR /code

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into the default location
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the code (The .dockerignore will skip your local .venv)
COPY . .

# Match your intended port
EXPOSE 8000

# Use uv run to execute the app
CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]










# # Use an official Python runtime as a parent image
# FROM python:3.13-slim

# LABEL maintainer="Zain ALi"
# # Set the working directory in the container
# WORKDIR /code

# # Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# # Install system dependencies required for potential Python packages
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy dependency files first for better caching
# COPY pyproject.toml uv.lock ./

# # Install dependencies
# ENV UV_VENV_DIR=/tmp/venv
# RUN /bin/uv sync --frozen --no-install-project

# # Copy the rest of the code
# COPY . /code/

# # Make port 8002 available to the world outside this container
# EXPOSE 8000

# # Run the app. CMD can be overridden when starting the container
# CMD /bin/uv run --venv /tmp/venv fastapi dev main.py --host 0.0.0.0
