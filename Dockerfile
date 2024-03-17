# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /splitwise

# Install dependencies
COPY requirements.txt /splitwise/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /splitwise/

# Expose port 8000 to allow communication to/from server
EXPOSE 8000