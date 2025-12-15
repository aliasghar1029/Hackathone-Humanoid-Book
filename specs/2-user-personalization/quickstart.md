# Quickstart Guide: Personalized Learning Platform

## Overview
This guide provides step-by-step instructions to set up and run the personalized learning platform with authentication, content personalization, and Urdu translation features.

## Prerequisites
- Node.js 18+ with npm
- Python 3.8+ with pip (for backend services)
- Better-Auth.com account and API keys
- OpenAI API key for translation services
- Git for version control

## Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Hackathone-Humanoid-Book.git
cd Hackathone-Humanoid-Book
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create `.env` files in both the root and backend directories:

**Root directory (.env):**
```env
# Better-Auth.com Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_TOKEN=your-better-auth-token

# OpenAI API Configuration
NEXT_PUBLIC_OPENAI_API_KEY=your-openai-api-key
NEXT_PUBLIC_OPENAI_ORG_ID=your-openai-org-id

# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api
```

**Backend directory (backend/.env):**
```env
# Better-Auth.com Configuration
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_URL=http://localhost:3000

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_ORG_ID=your-openai-org-id

# Database Configuration (if needed)
DATABASE_URL=your-database-url

# Subagent Configuration
SUBAGENT_API_KEY=your-subagent-api-key
```

## Running the Application

### 1. Start the Backend Server
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 2. Start the Frontend Development Server
```bash
npm run start
```

### 3. Alternative: Start Both Simultaneously
Use the provided startup script:
```bash
# On Unix/Linux/MacOS
./start-dev.sh

# On Windows
start-dev.bat
```

## Key Features Setup

### Authentication with Better-Auth.com
1. Sign up for Better-Auth.com and create an application
2. Add your domain to the allowed origins
3. Configure the authentication providers you want to use
4. Update the environment variables with your Better-Auth.com credentials

### Content Personalization
1. Personalization rules are loaded automatically based on user background
2. To add new personalization rules, update the `PersonalizationRule` entity in the data model
3. Rules are applied client-side for immediate responsiveness

### Urdu Translation
1. Translation uses OpenAI API for high-quality results
2. Translations are cached to improve performance and reduce API costs
3. The translation button appears at the beginning of each chapter

## API Endpoints

### Authentication
- `POST /api/auth/profile` - Update user profile with background information
- `GET /api/auth/session` - Get current user session information

### Personalization
- `GET /api/personalization/rules` - Get personalization rules for user
- `POST /api/personalization/apply` - Apply personalization to content

### Translation
- `POST /api/translate/to-urdu` - Translate content to Urdu
- `GET /api/translate/cache/{cacheId}` - Get cached translation

## Testing the Features

### 1. Test Authentication
1. Navigate to the signup page
2. Complete registration and specify your technical background (software-focused, hardware-focused, or mixed)
3. Verify that your profile is saved correctly

### 2. Test Personalization
1. Log in with your background preference
2. Navigate to any chapter
3. Verify that content is personalized based on your background
4. Use the personalization toggle to switch between personalized and standard views

### 3. Test Translation
1. Navigate to any chapter
2. Click the Urdu translation button
3. Verify that content is translated to Urdu while maintaining formatting
4. Use the translation toggle to switch between English and Urdu

## Troubleshooting

### Common Issues

**Issue**: Authentication not working
**Solution**: Verify Better-Auth.com configuration and environment variables

**Issue**: Translation API errors
**Solution**: Check OpenAI API key validity and rate limits

**Issue**: Personalization not applying
**Solution**: Verify user profile has background information set

**Issue**: Slow page load times
**Solution**: Check browser console for errors, verify caching is working

### Debugging
- Enable debug logging by setting `DEBUG=true` in environment variables
- Check browser console for client-side errors
- Check backend logs for server-side errors
- Verify all API endpoints are accessible

## Next Steps

1. Explore the documentation in the `/docs` directory
2. Review the API contracts in `/specs/2-user-personalization/contracts/`
3. Check out the data model in `/specs/2-user-personalization/data-model.md`
4. Review the full implementation plan in `/specs/2-user-personalization/plan.md`