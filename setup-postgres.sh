#!/bin/bash
# Setup PostgreSQL for Well-Path on macOS

set -e

echo "Setting up PostgreSQL for Well-Path..."

# Check if Postgres is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL not found. Installing via Homebrew..."
    brew install postgresql
    brew services start postgresql
else
    echo "PostgreSQL found. Starting service..."
    brew services start postgresql || true
fi

# Wait for Postgres to start
sleep 2

# Create database and user
echo "Creating database and user..."
psql -U postgres -c "CREATE DATABASE wellpath_db;" 2>/dev/null || echo "Database may already exist"
psql -U postgres -c "CREATE USER wellpath_user WITH PASSWORD 'wellpath_password';" 2>/dev/null || echo "User may already exist"

# Grant privileges
echo "Granting privileges..."
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE wellpath_db TO wellpath_user;"
psql -U postgres -c "ALTER SCHEMA public OWNER TO wellpath_user;"
psql -U postgres -d wellpath_db -c "GRANT ALL ON SCHEMA public TO wellpath_user;"

echo "✓ PostgreSQL setup complete!"
echo ""
echo "Connection details:"
echo "  Database: wellpath_db"
echo "  User:     wellpath_user"
echo "  Password: wellpath_password"
echo ""
echo "Export these env vars before running migrations:"
echo "  export POSTGRES_DB=wellpath_db"
echo "  export POSTGRES_USER=wellpath_user"
echo "  export POSTGRES_PASSWORD=wellpath_password"
