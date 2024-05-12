#!/bin/bash

# Define connection parameters
DB_USERNAME="postgres"
DB_NAME="postgres"
DB_HOST="localhost"
DB_PORT="5432" 

# Path to your SQL script
SQL_SCRIPT="./schema.sql"

# Execute SQL script using psql
psql -U "$DB_USERNAME" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -f "$SQL_SCRIPT"
