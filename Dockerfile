FROM python:3.11-slim

WORKDIR /app

# Install system libs needed by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Baumer wheel
COPY CamereConfig/baumer_neoapi-1.5.0-*.whl /app/

# Install Baumer neoAPI wheel
RUN pip install baumer_neoapi-1.5.0-*.whl

# Copy full project
COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
