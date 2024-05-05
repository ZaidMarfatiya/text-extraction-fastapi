# Text Extraction Service

This is a FastAPI-based text extraction service that can extract text from PDF, DOC, and DOCX files. It supports concurrent request handling and can accept both local file paths and public URLs as input. The service also sends an email notification to the user upon completion of their task. The project uses PostgreSQL as the database and includes database migrations.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       # API endpoint functions
│   ├── core/
│   │   └── email.py  # Email configuration
│   ├── crud/
│   │   # CRUD operation functions for each model
│   ├── db/
│   │   # Files related to database connection and SQLAlchemy configuration
│   ├── db_models/
│   │   # Model definitions
│   └── main.py  # FastAPI application entry point
└── migrations/
└── versions/
    # Database migration files

## Docker Setup

1. Build the Docker image:

   ```bash
   docker-compose build

2. Run the Docker containers:

    docker-compose up

    This will start the PostgreSQL database and the FastAPI application containers.

3. Apply database migrations (in a separate terminal):

    docker-compose exec web alembic upgrade head

    This will apply the database migrations to the PostgreSQL database.

4. The service will be available at http://localhost:8000.

## Usage

To extract text from a file, send a POST request to the /extract_text endpoint with the file or URL and the recipient's email address:

curl -X POST -F "file=@/path/to/file.pdf" -F "recipient_email=your@email.com" http://localhost:8000/extract_text

curl -X POST -F "file=https://example.com/file.docx" -F "recipient_email=your@email.com" http://localhost:8000/extract_text

The extracted text will be returned in the response body, and an email notification will be sent to the provided email address upon completion of the task.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

In this updated README.md file, the Docker setup instructions have been modified to use Docker Compose. The provided Dockerfile and docker-compose.yml files have been included.

The Dockerfile sets up the Python environment, installs dependencies, copies the application code, and specifies the command to run the FastAPI application with Uvicorn.

The docker-compose.yml file defines two services: `db` for the PostgreSQL database and `web` for the FastAPI application. The `web` service depends on the `db` service, and the application code is mounted as a volume for development purposes.

The README.md also includes instructions for applying database migrations after starting the containers.

Please note that you may need to adjust the environment variables and database configurations according to your specific setup.