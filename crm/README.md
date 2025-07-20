# CRM Task Scheduling Setup

This document outlines the setup for Task 4 of the Crons project, configuring a Celery task with Celery Beat to generate a weekly CRM report.

## Prerequisites
- **Python 3.12**: Ensure Python is installed.
- **Redis**: Install and run Redis server for Celery's message broker.
- **Virtual Environment**: Activate the project’s virtual environment.
- **Django Project**: Ensure the `alx-backend-graphql_crm` project is set up with migrations applied.

## Setup Instructions

1. **Install Redis**
   ```bash
   sudo apt-get update
   sudo apt-get install redis-server
   redis-cli ping  # Should output: PONG
   ```

2. **Install Dependencies**
   Install required Python packages:
   ```bash
   /alx-backend-graphql_crm/venv/bin/pip install celery django-celery-beat redis gql requests
   /alx-backend-graphql_crm/venv/bin/pip freeze >> requirements.txt
   ```

3. **Run Migrations**
   Apply database migrations for `django_celery_beat`:
   ```bash
   /alx-backend-graphql_crm/venv/bin/python /home/bunnye/alx-backend-graphql_crm/manage.py migrate
   ```

4. **Start Celery Worker**
   Run the Celery worker in a terminal:
   ```bash
   /alx-backend-graphql_crm/venv/bin/celery -A crm worker -l info
   ```

5. **Start Celery Beat**
   Run Celery Beat in a separate terminal:
   ```bash
   /alx-backend-graphql_crm/venv/bin/celery -A crm beat -l info
   ```

6. **Run Django Server**
   Start the Django development server for GraphQL queries:
   ```bash
   /alx-backend-graphql_crm/venv/bin/python /alx-backend-graphql_crm/manage.py runserver
   ```

7. **Verify Logs**
   Check the report logs:
   ```bash
   cat /tmp/crm_report_log.txt
   ```
   Expected output format:
   ```
   2025-07-14 06:00:00 - Report: 3 customers, 5 orders, 2499.95 revenue
   ```

## Troubleshooting
- Ensure Redis is running (`redis-cli ping`).
- Verify the Django server is accessible at `http://localhost:8000/graphql`.
- Check Celery worker and Beat logs for errors.
- Ensure `/tmp/crm_report_log.txt` is writable:
  ```bash
  touch /tmp/crm_report_log.txt
  chmod 666 /tmp/crm_report_log.txt
  ```