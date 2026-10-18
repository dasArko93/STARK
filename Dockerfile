# Lightweight Python base image optimized for Cloud Run
FROM python:3.11-slim

# Set environment variables for clean logging and default port
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Working directory inside the container
WORKDIR /app

# Install Python dependencies with layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application assets, source modules, and entrypoint
COPY src/ ./src/
COPY assets/ ./assets/
COPY app.py .
COPY README.md .

# Expose standard Cloud Run port
EXPOSE 8080

# Launch Streamlit with Cloud Run production flags
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false"]
