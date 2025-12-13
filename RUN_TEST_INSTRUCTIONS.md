# RAG Chatbot for Humanoid Robotics Textbook - Run & Test Instructions

## Backend Setup and Testing

### 1. Backend Local Development

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys (copy from `.env.example`):
```bash
cp .env.example .env
# Then edit .env with your actual API keys
```

5. Run the backend locally:
```bash
python app.py
# Or with uvicorn:
uvicorn app:app --reload --port 8000
```

6. The API will be available at `http://localhost:8000`

### 2. Ingest Documentation

1. To ingest all markdown files from the `docs/` folder:
```bash
python ingest.py
```

2. Verify ingestion by checking the API docs at `http://localhost:8000/docs` and testing the `/query` endpoint.

### 3. Test the API Endpoints

- Health check: `GET http://localhost:8000/health`
- API docs: `GET http://localhost:8000/docs`
- Query endpoint: `POST http://localhost:8000/query`
  - Body: `{"query": "your question", "selected_text": "optional selected text"}`
- Ingest endpoint: `POST http://localhost:8000/ingest`

## Frontend Integration and Testing

### 1. Docusaurus Setup

1. Make sure you have the ChatbotWidget component in `src/components/ChatbotWidget.jsx` and its CSS in `src/components/ChatbotWidget.css`.

2. The Layout wrapper is in `src/theme/Layout/index.js` which automatically includes the chatbot on all pages.

3. If you haven't already, install dependencies and start your Docusaurus site:
```bash
npm install
npm run start
```

### 2. Testing the Chatbot Widget

1. Visit your Docusaurus site (typically at `http://localhost:3000`)

2. You should see a floating chat button on the bottom right of every page

3. Click the button to open the chat interface

4. Test the following functionality:
   - Type a message and send it
   - Select text on the page and see it auto-fill in the chat
   - Ask questions about the humanoid robotics content
   - Verify that the "Selected" text preview appears when text is selected

5. Check the browser's developer console for any errors

## End-to-End Testing

### 1. Full Workflow Test

1. Start both the backend and frontend:
   - Backend: `uvicorn app:app --reload --port 8000`
   - Frontend: `npm run start`

2. Ingest the documentation:
```bash
python ingest.py
```

3. Open your browser and navigate to the Docusaurus site

4. Select some text from a documentation page

5. Open the chatbot and verify the selected text appears in the input

6. Ask a question related to the selected text and verify you get a relevant response

### 2. API Integration Test

1. With the backend running, test the query endpoint directly:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type": "application/json" \
  -d '{"query": "What is physical AI?", "selected_text": "Physical AI combines machine learning with physics"}'
```

2. Verify you get a proper response with sources.

## Troubleshooting

### Common Issues

1. **Backend not connecting to services:**
   - Verify all API keys in `.env` are correct
   - Check that Qdrant, Neon, and Cohere services are accessible
   - Look for specific error messages in the backend console

2. **Frontend can't connect to backend:**
   - Ensure the backend is running and accessible
   - Check the fetch URL in `ChatbotWidget.jsx` matches your backend URL
   - Look for CORS errors in the browser console

3. **No results from queries:**
   - Verify documents were properly ingested
   - Check that the Qdrant collection has vectors stored
   - Ensure embeddings are being generated correctly

4. **Text selection not working:**
   - Check browser console for JavaScript errors
   - Verify the text selection event listeners are working

### Verification Steps

1. Check that the backend is running: `curl http://localhost:8000/health`

2. Verify API keys are working by testing individual services (Cohere, Qdrant, Gemini)

3. Confirm documents are in Qdrant by using the Qdrant dashboard or API

4. Test that the frontend can communicate with the backend using browser dev tools

## Production Deployment

### 1. Backend Deployment

1. Follow the instructions in `backend/VERCEL_DEPLOYMENT.md`

2. Update the frontend to use the deployed backend URL

### 2. Frontend Deployment

1. Update the fetch URL in `ChatbotWidget.jsx` to point to your deployed backend

2. Build and deploy your Docusaurus site as usual

3. Test the complete flow on the deployed site

## Performance Testing

1. Test with multiple concurrent users if needed
2. Monitor response times for queries
3. Check that the vector database performs well with your content size
4. Verify that the chat interface remains responsive

## Security Considerations

1. Never commit API keys to version control
2. Use environment variables for all sensitive information
3. Implement proper rate limiting in production
4. Add authentication if needed for your use case