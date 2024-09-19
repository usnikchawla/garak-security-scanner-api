# Garak Security Scanner API for AWS-Deployed Generative Models: Setup and Usage Report

## Table of Contents
1. Introduction
2. Prerequisites
3. System Architecture
4. API Setup
5. Database Setup
6. AWS Integration
7. Garak Integration
8. API Endpoints Implementation
9. Background Task Processing
10. Testing and Validation
11. Deployment
12. Usage Guide
13. Maintenance and Monitoring
14. Security Considerations
15. Conclusion

## 1. Introduction

This report details the process of setting up and using a custom API for the Garak Security Scanner, designed to test generative AI models deployed on AWS Bedrock and Amazon SageMaker. The API provides a scalable and flexible solution for managing models, configurations, and security scans.

## 2. Prerequisites

Before beginning the setup process, ensure the following prerequisites are met:

- Python 3.8 or higher
- AWS account with access to Bedrock and SageMaker
- AWS CLI installed and configured
- Docker (for containerization)
- Redis (for background task processing)
- PostgreSQL (for database)

## 3. System Architecture

The system consists of the following components:

- Flask-based RESTful API
- PostgreSQL database for data persistence
- Celery for background task processing
- Redis as a message broker for Celery
- AWS SDK (boto3) for interacting with AWS services
- Garak library for security scanning

## 4. API Setup

1. Create a new Python virtual environment:
   ```
   python -m venv garak-api-env
   source garak-api-env/bin/activate
   ```

2. Install required packages:
   ```
   pip install flask flask-restx sqlalchemy psycopg2-binary boto3 garak celery redis
   ```

3. Set up the basic Flask application structure:
   - Create `app.py` as the main entry point
   - Set up Flask-RESTX for API documentation
   - Define namespaces for models, configurations, and scans

## 5. Database Setup

1. Install and configure PostgreSQL

2. Create a new database for the application:
   ```sql
   CREATE DATABASE garak_api;
   ```

3. Set up SQLAlchemy ORM models:
   - Create `models.py` file
   - Define Model, Config, and Scan classes
   - Implement database connection and session management

## 6. AWS Integration

1. Configure AWS credentials:
   ```
   aws configure
   ```

2. Set up boto3 clients for Bedrock and SageMaker in the application

3. Implement functions to validate model endpoints during registration

## 7. Garak Integration

1. Install Garak library:
   ```
   pip install garak
   ```

2. Implement Garak configuration setup in the scan execution process

3. Create utility functions to convert between Garak and API data structures

## 8. API Endpoints Implementation

Implement the following endpoints:

1. Model Management:
   - POST /models (Create a new model)
   - GET /models (List all models)
   - GET /models/<id> (Get a specific model)
   - DELETE /models/<id> (Delete a model)

2. Configuration Management:
   - POST /configs (Create a new configuration)
   - GET /configs (List all configurations)
   - GET /configs/<id> (Get a specific configuration)
   - DELETE /configs/<id> (Delete a configuration)

3. Scan Management:
   - POST /scans (Create a new scan)
   - GET /scans (List all scans)
   - GET /scans/<id> (Get a specific scan)

## 9. Background Task Processing

1. Set up Celery for background task processing:
   - Configure Redis as the message broker
   - Create Celery tasks for running Garak scans

2. Implement scan execution logic:
   - Fetch model and configuration details
   - Set up Garak configuration
   - Run the scan
   - Update scan status and results in the database

## 10. Testing and Validation

1. Implement unit tests for each API endpoint

2. Create integration tests to verify the entire scan process

3. Perform load testing to ensure the API can handle multiple concurrent requests

## 11. Deployment

1. Containerize the application:
   - Create a Dockerfile
   - Build and test the Docker image locally

2. Set up AWS ECS (Elastic Container Service):
   - Create an ECS cluster
   - Define task definitions for the API and worker containers
   - Create an ECS service to run the containers

3. Set up AWS Application Load Balancer:
   - Create a target group for the API containers
   - Configure the load balancer to route traffic to the target group

## 12. Usage Guide

1. Register a model:
   ```
   POST /models
   {
     "type": "bedrock",
     "name": "anthropic.claude-v2",
     "endpoint": "https://bedrock-runtime.us-west-2.amazonaws.com"
   }
   ```

2. Create a configuration:
   ```
   POST /configs
   {
     "name": "Default Scan",
     "probes": ["InjectProbe", "LeakProbe"],
     "detectors": ["ExfiltrationDetector", "JailbreakDetector"]
   }
   ```

3. Initiate a scan:
   ```
   POST /scans
   {
     "model_id": "1",
     "config_id": "1",
     "prompt": "What is the capital of France?"
   }
   ```

4. Retrieve scan results:
   ```
   GET /scans/1
   ```

## 13. Maintenance and Monitoring

1. Set up CloudWatch for logging and monitoring:
   - Configure log groups for API and worker containers
   - Create CloudWatch alarms for important metrics (e.g., API response time, error rates)

2. Implement regular database backups

3. Set up automated security patching for the ECS instances

## 14. Security Considerations

1. Implement API authentication and authorization:
   - Use AWS Cognito or a similar service for user management
   - Implement JWT-based authentication for API requests

2. Encrypt sensitive data at rest and in transit:
   - Use AWS KMS for managing encryption keys
   - Enable SSL/TLS for all API communications

3. Implement proper IAM roles and policies:
   - Create least-privilege IAM roles for ECS tasks
   - Use IAM roles for EC2 instances running ECS tasks

4. Regularly update dependencies and apply security patches

## 15. Conclusion

This report outlines the process of setting up and using a custom Garak Security Scanner API for AWS-deployed generative models. By following these steps, you can create a scalable and secure solution for managing and executing security scans on your AI models. Regular maintenance, monitoring, and security updates are crucial for ensuring the long-term reliability and safety of the system.
