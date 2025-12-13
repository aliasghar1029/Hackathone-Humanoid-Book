@echo off
echo Starting RAG Chatbot development environment...

REM Start backend in a new window
start "Backend Server" cmd /k "cd backend && python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
start "Frontend Server" cmd /k "npm run start"

echo Both services should now be running:
echo.  - Backend: http://127.0.0.1:8000
echo.  - Frontend: http://localhost:3000 (or as shown in npm output)
echo.
echo Close this window or press Ctrl+C in both terminals to stop the services
pause