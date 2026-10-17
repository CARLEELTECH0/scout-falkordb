FROM python:3.12-slim

WORKDIR /app

# Install system build dependencies for C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY scout/ ./scout/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY run.py .
COPY README.md .
COPY .env.example .env

# Expose FastAPI REST & Interactive Visualizer port
EXPOSE 8000

# Seed the graph on container startup and launch the visualizer
CMD ["sh", "-c", "python run.py seed && python run.py serve ${PORT:-8000}"]
