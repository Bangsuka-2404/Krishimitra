# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /code

# Install system dependencies (needed for OpenCV/Pillow if necessary)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set permissions for the HF user (required for Spaces)
RUN chmod -R 777 /code

# Expose the port (HF uses 7860 by default)
EXPOSE 7860

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
