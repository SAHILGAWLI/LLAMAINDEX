# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (add more if needed)
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose the port (Render will set $PORT, but 8000 is default for FastAPI)
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "query_api:app", "--host", "0.0.0.0", "--port", "8000"]
