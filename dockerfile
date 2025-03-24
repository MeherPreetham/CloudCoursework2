FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY function_app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Use Gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "function_app:app"]
