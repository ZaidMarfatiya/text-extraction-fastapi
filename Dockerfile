# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    apt-utils 

# Copy the application code into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Give executable permission to entrypoint
RUN ["chmod", "+x", "/app/entrypoint.sh"]

# Set the command to start the FastAPI app with Uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]
