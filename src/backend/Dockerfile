# Use an official Python runtime as a parent image
FROM python:3.10-slim AS builder

# Set the working directory in the container
WORKDIR /app
RUN pip install --upgrade pip

# Copy only the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-slim
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Set up working directory
WORKDIR /app

# Copy application code
COPY app.py /app

# Default command to run your application
CMD ["python", "app.py"]
