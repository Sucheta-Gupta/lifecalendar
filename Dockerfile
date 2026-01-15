# Use a small official Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
COPY Arial.ttf .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY main.py .

# Expose the port that Render/Fly.io/Railway will use
EXPOSE 8080

# Set the start command inside the Dockerfile
# Uvicorn will run the FastAPI app on 0.0.0.0:8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
