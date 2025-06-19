FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ build-essential python3-dev tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from backend folder and install dependencies
COPY rest_api/requirements.txt ./rest_api/requirements.txt
RUN pip install --no-cache-dir -r rest_api/requirements.txt

# Install scispaCy model
RUN pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz

# Copy the full project into the container
COPY . .

# Move to backend code directory
WORKDIR /app/rest_api

# Add root directory to Python path
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]