# Running the Physical AI & Humanoid Robotics Textbook

## Development Setup

This project consists of two main components:
1. **Frontend**: Docusaurus-based documentation site (runs on port 3000)
2. **Backend**: FastAPI server with AI features (runs on port 8000)

## Running in Development

### Option 1: Full Setup (Recommended)
To use all features including backend AI processing:

1. **Start the Backend Server**:
   ```bash
   python run_server.py
   ```
   This will start the backend server on `http://127.0.0.1:8000`

2. **Start the Frontend Server** (in a separate terminal):
   ```bash
   npm run start
   ```
   This will start the frontend on `http://localhost:3000`

### Option 2: Frontend Only
To run just the frontend with client-side features:
```bash
npm run start
```
The frontend will work with client-side authentication, personalization, and translation fallbacks.

## Proxy Configuration

The frontend is configured to proxy API requests to the backend:
- `/api/**` → `http://127.0.0.1:8000/api/**`
- `/query` → `http://127.0.0.1:8000/query`
- `/ingest` → `http://127.0.0.1:8000/ingest`
- `/health` → `http://127.0.0.1:8000/health`

When the backend is not running, API calls will fail gracefully and fallback mechanisms will be used.

## Required Environment Variables

Create a `.env` file in the root directory with:
```
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
DATABASE_URL=your_database_url_here
```

For client-side only usage, you can set the Gemini API key in browser localStorage:
```javascript
localStorage.setItem('gemini_api_key', 'your_gemini_api_key_here');
```

## Features Available

### Client-Side Only:
- User authentication with localStorage
- Content personalization based on user background
- Urdu translation with Gemini API fallback
- Chapter controls for personalization/translation
- Chatbot widget

### With Backend:
- All client-side features plus:
- Advanced personalization with AI
- Backend translation with caching
- Document ingestion and RAG
- User profile management
- API-based authentication