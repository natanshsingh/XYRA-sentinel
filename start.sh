#!/bin/bash
echo "Starting XYRA Sentinel System..."

# Activate virtual environment if available
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the FastAPI server which also hosts the frontend statically
echo "Starting FastAPI integrated server..."
echo "Access the 3D Dashboard at: http://localhost:8000"
uvicorn api.integrated_server:app --host 0.0.0.0 --port 8000 --reload
