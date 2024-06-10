# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the server will listen on
EXPOSE 8080

# set export PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED=1

# Set the command to run the server when the container starts
CMD ["python", "main.py"]
