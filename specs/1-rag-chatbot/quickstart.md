# Quickstart Guide: RAG Chatbot Integration

## Prerequisites

- Node.js (v18.0 or higher)
- Python (v3.8 or higher)
- Git
- Access to OpenAI-compatible API (e.g., Google Gemini API)
- Qdrant Cloud account (Free Tier)
- Neon Serverless Postgres account

## Environment Setup

### Backend Environment Variables

Create `.env` file in the `backend` directory:

```env
# Qdrant Configuration
QDRANT_URL=your-qdrant-cluster-url
QDRANT_API_KEY=your-qdrant-api-key

# OpenAI-Compatible API (e.g., Google Gemini)
GEMINI_API_KEY=your-gemini-api-key

# Cohere for embeddings (alternative to OpenAI embeddings)
COHERE_API_KEY=your-cohere-api-key

# Database Configuration
DATABASE_URL=your-neon-postgres-connection-string

# JWT Secret for session management
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256

# Application Configuration
PORT=8000
HOST=0.0.0.0
```

### Frontend Environment Variables

Update `.env` file in the project root if needed:

```env
# Proxy configuration handled via docusaurus config
# No additional frontend environment variables needed
```

## Installation Steps

### 1. Clone and Setup Repository

```bash
git clone <repository-url>
cd <repository-name>
npm install
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Or if requirements.txt doesn't exist, install these packages:
pip install fastapi uvicorn qdrant-client cohere psycopg2-binary python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 3. Database Initialization

```bash
# Make sure your Neon Postgres instance is created
# The application will automatically create required tables on startup
```

### 4. Vector Store Setup

```bash
# The application will automatically create the Qdrant collection on first run
# Make sure your QDRANT_URL and QDRANT_API_KEY are properly configured
```

## Running the Application

### 1. Start the Backend Server

```bash
# From the backend directory
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Docusaurus Frontend

```bash
# From the project root
npm run start
```

### 3. Access the Application

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Backend API documentation: `http://localhost:8000/docs`

## Content Ingestion

### Automatic Ingestion

The system will automatically index all content from your Docusaurus docs directory:

```bash
# To trigger content ingestion, make a POST request to:
curl -X POST http://localhost:8000/api/content/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "docs/intro.md",
    "content": "Full content of the document...",
    "metadata": {
      "title": "Introduction",
      "source": "docs/intro.md",
      "page_number": 1
    }
  }'
```

### Batch Ingestion

A script will be available to ingest all existing documentation:

```bash
# From the backend directory
python ingest.py
```

## API Endpoints

### Chat Endpoint

```bash
# Send a query to the chatbot
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is humanoid robotics?",
    "selected_text": "Optional selected text context",
    "session_id": "Optional session ID"
  }'
```

### Session Management

```bash
# Get conversation history
curl -X GET http://localhost:8000/api/chat/session/{sessionId}
```

## Frontend Integration

The chatbot widget will be automatically integrated into all Docusaurus pages through the custom Layout component. No additional setup required.

## Troubleshooting

### Common Issues

1. **Connection Refused Errors**
   - Make sure backend server is running on port 8000
   - Check that proxy configuration is correct

2. **API Key Errors**
   - Verify all API keys are properly set in environment variables
   - Check for typos in API key values

3. **Qdrant Connection Issues**
   - Verify QDRANT_URL and QDRANT_API_KEY
   - Check that the cluster is active and accessible

4. **Database Connection Issues**
   - Verify DATABASE_URL is properly formatted
   - Check that Neon Postgres instance is active