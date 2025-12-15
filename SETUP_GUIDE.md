# Physical AI & Humanoid Robotics Book - Setup and Configuration Guide

## Environment Variables (.env)

### Backend Configuration (backend/.env)
```
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_connection_string
```

### Required API Keys and Services

1. **Qdrant Vector Database**
   - URL to your Qdrant instance
   - API key for authentication
   - Used for vector storage and similarity search

2. **Cohere API**
   - API key for embedding generation
   - Used with embed-english-v3.0 model
   - Generates 1024-dimensional vectors

3. **Google Gemini API**
   - API key for AI responses and translation
   - Used with gemini-1.5-flash model
   - Handles Q&A and translation services

4. **PostgreSQL Database**
   - Connection string for user data storage
   - Stores user profiles and authentication data

## Project Structure

```
Physical-AI-Humanoid-Book/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main application
│   ├── auth.py             # Authentication endpoints
│   ├── personalization.py  # Personalization endpoints
│   ├── translation.py      # Translation endpoints
│   ├── subagents/          # Subagent architecture
│   │   ├── api.py
│   │   ├── personalization_agent.py
│   │   └── translation_agent.py
│   ├── skills/             # Reusable skills
│   │   ├── personalization_skills.py
│   │   └── translation_skills.py
│   └── requirements.txt    # Python dependencies
├── src/                    # Docusaurus frontend
│   ├── components/         # React components
│   │   ├── Auth/           # Authentication components
│   │   ├── Personalization/ # Personalization components
│   │   ├── Translation/    # Translation components
│   │   ├── ChatbotWidget.jsx # Main chat interface
│   │   └── ChapterHeaderControls.js # Chapter controls
│   ├── contexts/           # React contexts
│   │   └── AuthContext.js  # Authentication context
│   └── plugins/            # Docusaurus plugins
│       └── proxyPlugin.js  # API proxy configuration
├── docusaurus.config.js    # Docusaurus configuration
├── package.json           # Frontend dependencies
└── run_server.py          # Backend startup script
```

## Dependencies

### Backend (requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
qdrant-client>=1.9.0
cohere>=4.4.0
openai>=1.10.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
pydantic>=2.5.0
python-dotenv>=1.0.0
tiktoken>=0.5.0
python-multipart>=0.0.6
```

### Frontend (package.json)
```
@docusaurus/core: 3.9.2
@docusaurus/preset-classic: 3.9.2
@mdx-js/react: ^3.0.0
better-auth: ^1.4.7
clsx: ^2.0.0
framer-motion: ^11.0.0
prism-react-renderer: ^2.3.0
react: ^19.0.0
react-dom: ^19.0.0
react-intersection-observer: ^9.5.3
```

## API Endpoints Summary

### Main Endpoints
- `POST /query` - RAG chatbot (main functionality)
- `POST /ingest` - Document ingestion
- `GET /health` - System health check

### Authentication Endpoints
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout
- `GET /api/auth/me` - Get user profile
- `PUT /api/auth/profile` - Update profile

### Personalization Endpoints
- `POST /api/personalization/personalize-content`
- `POST /api/personalization/analyze-and-personalize`
- `GET /api/personalization/user-profile-rules/{background}`

### Translation Endpoints
- `POST /api/translate/to-urdu`
- `GET /api/translate/cache/{cache_id}`
- `DELETE /api/translate/cache/clear`

### Subagent Endpoints
- `POST /api/subagents/personalize`
- `POST /api/subagents/translate`
- `POST /api/subagents/analyze-content`
- `POST /api/subagents/adapt-for-user`

## Running the Application

### Backend
```bash
cd backend
pip install -r requirements.txt
python run_server.py
# Or: uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm install
npm start
# Or: docusaurus start --host 0.0.0.0 (to access from other devices)
```

## Key Features Configuration

### RAG Chatbot
- Uses Qdrant for vector storage
- Cohere for embedding generation
- Gemini for response generation
- Supports selected text context
- Implements timeout handling (45-60 seconds)

### Personalization System
- User background: software-focused, hardware-focused, mixed, beginner
- Content adaptation based on user profile
- Complexity adjustment and terminology modification
- Example addition based on user interests

### Translation System
- Urdu translation support
- Quality validation and postprocessing
- Caching mechanism for performance
- Context preservation for technical terms

### Authentication
- Token-based session management
- Background and preference collection
- Profile management capabilities
- Protected content access

## Troubleshooting

### Common Issues
1. **API Keys Not Set**: Ensure all required environment variables are set
2. **Qdrant Connection**: Verify QDRANT_URL and QDRANT_API_KEY are correct
3. **CORS Issues**: Check that frontend and backend are properly configured
4. **Timeout Errors**: Increase timeout values if needed for complex queries

### Health Checks
- `/health` - Overall system health
- `/api/auth/health` - Authentication service
- `/api/translate/health` - Translation service
- `/api/subagents/health` - Subagent services
- `/api/personalization/health` - Personalization service

## Security Considerations
- Store API keys securely, never commit to version control
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Validate and sanitize all user inputs
- Regularly rotate API keys