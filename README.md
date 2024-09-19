# Garak AWS Bedrock Scanner API

This project implements an API for running Garak security scans on AWS Bedrock models.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/garak-aws-project.git
   cd garak-aws-project
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your .env file with the necessary environment variables (see .env.example).

5. Set up a PostgreSQL database and update the DATABASE_URL in your .env file.

6. Run database migrations:
   ```
   flask db upgrade
   ```

7. Start the Celery worker:
   ```
   celery -A celery_worker.celery worker --loglevel=info
   ```

8. Start the Flask application:
   ```
   python app.py
   ```

## Usage

The API provides endpoints for managing configurations, models, and running scans. 
Refer to the API documentation at `http://localhost:5000` when the application is running.

## Testing

Run the tests using:
```
pytest
```

## Deployment

For production deployment, consider using Gunicorn as the WSGI server:
```
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

Ensure you have set up appropriate security groups and network access controls in your AWS environment.
