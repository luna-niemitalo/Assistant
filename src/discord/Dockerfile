# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update
RUN apt install gcc wget libmariadb3 libmariadb-dev -y

RUN pip install --upgrade pip

# Copy only the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Set up working directory
WORKDIR /app

# Copy application code
COPY ./ /app

# Default command to run your application
CMD ["python","-u", "app.py"]