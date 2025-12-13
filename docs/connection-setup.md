# Start the RAG Chatbot Backend and Frontend Simultaneously

This project uses a FastAPI backend with a Docusaurus frontend. To run both services simultaneously for development:

## Prerequisites
- Python 3.8+ with pip
- Node.js 18+ with npm
- All required API keys in the backend/.env file

## Setup

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up your environment variables in `backend/.env`:
   ```env
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   GEMINI_API_KEY=your_gemini_api_key
   DATABASE_URL=your_database_url
   ```

### Frontend Setup
1. Install Node.js dependencies: `npm install`
2. The Docusaurus proxy is configured to forward API requests to the backend

## Running the Application

### Method 1: Separate Terminals
1. Terminal 1 - Start the backend: `cd backend && python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload`
2. Terminal 2 - Start the frontend: `npm run start`

### Method 2: Using the startup script
1. Run: `npm run dev` (if added to package.json) or use a process manager like PM2

## API Endpoints
- Health check: `GET http://127.0.0.1:8000/health`
- Query: `POST http://127.0.0.1:8000/query`
- Ingest: `POST http://127.0.0.1:8000/ingest`

## Troubleshooting
- If the backend is not responding, ensure it's running on port 8000
- Check that all required environment variables are set
- Verify that the Docusaurus proxy configuration in `src/plugins/proxyPlugin.js` is correct
- Look for CORS errors in browser console if requests are failing