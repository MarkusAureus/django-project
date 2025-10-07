#!/bin/sh

# This script waits for the database to be ready before executing the main command.

# The 'db' hostname is the service name from docker-compose.yml
# The -U and -p flags specify the user and password from the environment variables.
until pg_isready -h "db" -p "5432" -U "${POSTGRES_USER}"; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready!"

# Execute the command passed to this script
exec "$@"

