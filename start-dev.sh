#!/bin/bash

# Script to start both backend and frontend for development

echo "Starting RAG Chatbot development environment..."

# Function to handle cleanup on exit
cleanup() {
    echo "Stopping services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "Services stopped."
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend in the background
echo "Starting backend server..."
cd backend
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in the background
echo "Starting frontend server..."
npm run start &
FRONTEND_PID=$!

echo "Both services are running:"
echo "- Backend: http://127.0.0.1:8000"
echo "- Frontend: http://localhost:3000 (or as shown in npm output)"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID