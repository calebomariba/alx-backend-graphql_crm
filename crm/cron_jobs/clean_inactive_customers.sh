#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$PROJECT_DIR" || {
    echo "Failed to navigate to project root: $PROJECT_DIR"
    exit 1
}

cwd=$(pwd)

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

DELETED_COUNT=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer
cutoff_date = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(order__isnull=True, created_at__lte=cutoff_date).delete()
print(deleted)
")

if [ -n "$DELETED_COUNT" ]; then
    echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$TIMESTAMP - Failed to delete customers or none found" >> /tmp/customer_cleanup_log.txt
fi