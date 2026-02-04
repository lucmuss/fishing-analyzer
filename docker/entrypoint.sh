#!/bin/bash
set -e

# Start MongoDB in background
mongod --dbpath /data/db --fork --logpath /data/db/log

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to start..."
sleep 5

# Run data import (migrations equivalent)
echo "Running data import..."
python install.py

# Run the application
echo "Starting application..."
python run.py