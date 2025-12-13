# Deploying the RAG Chatbot Backend to Vercel

This guide will walk you through deploying the FastAPI backend to Vercel as a serverless function.

## Prerequisites

1. Install the Vercel CLI globally:
```bash
npm install -g vercel
```

2. Log in to your Vercel account:
```bash
vercel login
```

## Deployment Steps

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a `vercel.json` configuration file in the backend directory:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

3. Create the `vercel.json` file:
```bash
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
EOF
```

4. Add environment variables to Vercel:
```bash
vercel env add QDRANT_URL production
vercel env add QDRANT_API_KEY production
vercel env add COHERE_API_KEY production
vercel env add GEMINI_API_KEY production
vercel env add DATABASE_URL production
```

Follow the prompts to enter your actual API keys and connection strings for each variable.

5. Deploy to Vercel:
```bash
vercel --prod
```

This will deploy your backend to a URL like `https://your-project-name.vercel.app`

6. Update the frontend to use the deployed backend URL by modifying the fetch URL in `src/components/ChatbotWidget.jsx`:
Change:
```javascript
const response = await fetch('https://hackathone-humanoid-book-backend.vercel.app/query', {
```
To:
```javascript
const response = await fetch('YOUR_DEPLOYED_VERCEL_URL/query', {
```

## Alternative Deployment via Git

Instead of using the CLI, you can also deploy by connecting your GitHub repository to Vercel:

1. Push your backend code to a GitHub repository
2. Go to [vercel.com](https://vercel.com) and click "New Project"
3. Import your backend repository
4. In the configuration:
   - Framework: None (or Python)
   - Root Directory: backend/
5. Add the environment variables as specified in step 4
6. Click "Deploy"

## Verification

After deployment, you can verify your API is working by visiting:
- Health check: `https://your-deployed-url.vercel.app/health`
- API docs: `https://your-deployed-url.vercel.app/docs`

## Environment Variables

Make sure to set these environment variables in your Vercel project:

- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `COHERE_API_KEY`: Your Cohere API key
- `GEMINI_API_KEY`: Your Gemini API key
- `DATABASE_URL`: Your Neon Postgres connection string

## Note

For production use, make sure to update the CORS settings in `app.py` to only allow your domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Replace with your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```