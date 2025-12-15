# Physical AI & Humanoid Robotics Docusaurus Book - Comprehensive Feature Specification

## Project Overview
The Physical AI & Humanoid Robotics Docusaurus book is an educational platform built with Docusaurus (frontend) and FastAPI (backend). It features advanced AI capabilities including a RAG chatbot, content personalization, translation services, and authentication. The platform serves as an interactive textbook with intelligent features to enhance the learning experience.

## Architecture Overview

### Backend Stack
- **Framework**: FastAPI
- **AI Models**:
  - Gemini 1.5 Flash (for responses and translation)
  - Cohere embed-english-v3.0 (for embeddings)
- **Vector Database**: Qdrant
- **Database**: PostgreSQL (for user data)
- **Authentication**: Custom token-based system

### Frontend Stack
- **Framework**: Docusaurus v3.9.2
- **UI Components**: React with Bootstrap
- **State Management**: React Context API
- **Proxy**: Webpack dev server proxy for API communication

## Core Features

### 1. RAG Chatbot (Primary Feature)

#### Functionality
- **Purpose**: Provide intelligent Q&A about the Physical AI & Humanoid Robotics textbook
- **Input**: User queries, optionally with selected text from the page
- **Output**: Context-aware responses based on textbook content
- **Technology**: Retrieval-Augmented Generation using vector search

#### Technical Implementation
- **Query Processing**:
  - User query → Cohere embedding → Qdrant vector search → Context retrieval → Gemini response
- **Selected Text Priority**: When text is selected, the system prioritizes search results related to that text
- **Response Generation**: Uses gemini-1.5-flash with 800 max tokens and 0.7 temperature
- **Timeout Configuration**: 45-second timeout for API calls

#### User Experience
- Floating chat widget accessible from any page
- Text selection integration - selected text automatically appears in chat
- Loading indicators and error handling
- Source attribution for responses

### 2. User Authentication System

#### Functionality
- **Purpose**: User management and profile storage for personalization
- **Features**:
  - User registration with background information
  - Login/logout functionality
  - Profile management
  - Session management

#### Technical Implementation
- **Storage**: In-memory session tokens with PostgreSQL for user data
- **Background Collection**: Captures user's focus (software-focused, hardware-focused, mixed, beginner)
- **Additional Preferences**: Hardware, experience level, preferred language
- **Security**: Token-based authentication with session invalidation

#### User Experience
- Signup form with background selection
- Login modal
- Profile management interface
- Protected content access

### 3. Content Personalization

#### Functionality
- **Purpose**: Adapt content based on user's background and preferences
- **Personalization Rules**:
  - Software-focused: Emphasizes code implementations, algorithms, software architecture
  - Hardware-focused: Emphasizes physical components, electrical characteristics, mechanical systems
  - Mixed: Balances both software and hardware perspectives
  - Beginner: Simplifies content, focuses on fundamentals

#### Technical Implementation
- **Agent System**: PersonalizationAgent with rule-based transformations
- **Content Analysis**: Complexity scoring, content type identification, key concept extraction
- **Adaptation Logic**: Modifies technical depth, examples, and terminology based on user profile
- **Integration**: Works with both real-time API calls and content transformation

#### User Experience
- Personalize button in chapter controls
- Content adaptation based on user profile
- Reset functionality to original content
- Visual indicators of applied personalization

### 4. Urdu Translation

#### Functionality
- **Purpose**: Translate educational content to Urdu for accessibility
- **Target**: Full chapters or selected content
- **Quality**: Professional-grade translation using Gemini

#### Technical Implementation
- **Translation Agent**: Uses gemini-1.5-flash for translation
- **Validation**: Quality scoring and error detection
- **Postprocessing**: Formatting and consistency improvements
- **Caching**: Translation caching for performance optimization
- **Context Preservation**: Maintains technical terminology and structure

#### User Experience
- Translate to Urdu button in chapter controls
- Quality indicators for translations
- Reset to English functionality
- Error handling for failed translations

### 5. Subagent Architecture

#### Functionality
- **Purpose**: Modular AI agents for specialized tasks
- **Components**:
  - Personalization Agent: Handles content adaptation
  - Translation Agent: Manages content translation
  - Content Analysis Agent: Analyzes content characteristics

#### Technical Implementation
- **Modular Design**: Separate agents for different capabilities
- **Skill System**: Reusable functions for common tasks
- **API Integration**: REST endpoints for each agent capability
- **Error Handling**: Fallback mechanisms when agents fail

## Technical Infrastructure

### API Endpoints

#### Main Query Endpoint
- **Path**: `POST /query`
- **Functionality**: Core RAG chatbot functionality
- **Parameters**: query, selected_text, user_background, target_language, personalization_enabled, translation_enabled
- **Response**: Answer with sources, personalization/translation indicators

#### Authentication Endpoints
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout
- `GET /api/auth/me` - Get user profile
- `PUT /api/auth/profile` - Update user profile

#### Personalization Endpoints
- `POST /api/personalization/personalize-content` - Content personalization
- `POST /api/personalization/analyze-and-personalize` - Analysis and personalization
- `GET /api/personalization/user-profile-rules/{background}` - Get personalization rules

#### Translation Endpoints
- `POST /api/translate/to-urdu` - Translate to Urdu
- `GET /api/translate/cache/{cache_id}` - Get cached translation
- `DELETE /api/translate/cache/clear` - Clear cache

#### Subagent Endpoints
- `POST /api/subagents/personalize` - Personalization subagent
- `POST /api/subagents/translate` - Translation subagent
- `POST /api/subagents/analyze-content` - Content analysis
- `POST /api/subagents/adapt-for-user` - User-specific adaptation

### Database Schema

#### Vector Database (Qdrant)
- **Collection**: documents
- **Vector Size**: 1024 dimensions (Cohere embed-english-v3.0)
- **Distance**: Cosine similarity
- **Payload**: content, metadata (title, source, page_number, chunk_id)

#### Relational Database (PostgreSQL)
- **Table**: documents
- **Fields**: id, file_path, title, created_at

#### In-Memory Storage
- **Sessions**: token-based session management
- **Translation Cache**: cached translations for performance

### Frontend Integration

#### Components
- **ChatbotWidget**: Floating chat interface with text selection
- **AuthButton**: Authentication controls
- **PersonalizeButton**: Content personalization controls
- **UrduTranslationButton**: Translation controls
- **ChapterHeaderControls**: Combined controls for chapter features

#### State Management
- **AuthContext**: User authentication and profile management
- **Content State**: Dynamic content modification for personalization/translation

#### API Communication
- **Proxy Configuration**: Webpack proxy to backend API
- **Error Handling**: Comprehensive error handling and user feedback
- **Loading States**: Visual indicators for processing operations

## Security Considerations

### Authentication Security
- Token-based session management
- Secure session invalidation
- Input validation and sanitization

### API Security
- Rate limiting considerations
- Input sanitization (removes special characters, newlines)
- Environment variable management for API keys

### Data Privacy
- User data stored securely
- Background information used only for personalization
- No sensitive data transmitted unnecessarily

## Performance Optimizations

### Caching
- Translation result caching
- Vector search result optimization
- Content transformation caching

### Resource Management
- Background processing for document ingestion
- Efficient vector search with limited results (5 max)
- Context truncation to prevent token limits
- Asynchronous processing where possible

### Timeout Management
- 30-second timeout for Cohere calls
- 45-60 second timeouts for Gemini calls
- Request cancellation for long-running operations

## Error Handling and Resilience

### Service Degradation
- Graceful fallback when AI services are unavailable
- Mock responses when services fail
- Comprehensive error logging

### Client-Side Resilience
- Network error handling
- Timeout error messages
- Fallback to original content when transformations fail

### Health Monitoring
- Health check endpoints for all services
- Service status monitoring
- Dependency health verification

## Deployment and Configuration

### Environment Variables
- `QDRANT_URL` and `QDRANT_API_KEY` for vector database
- `COHERE_API_KEY` for embedding generation
- `GEMINI_API_KEY` for AI responses
- `DATABASE_URL` for PostgreSQL connection

### CORS Configuration
- Multiple allowed origins for development and production
- Credentials enabled for authentication
- All methods and headers allowed

### Startup Configuration
- Automatic collection initialization
- Service health verification
- Client initialization with error handling

## Future Extensibility

### Plugin Architecture
- Modular subagent system
- Skill-based functionality
- Easy addition of new AI capabilities

### Internationalization
- Translation framework ready for additional languages
- Localization support in UI components

### Personalization Expansion
- Rule-based system for easy addition of new personalization types
- Content analysis capabilities for new adaptation strategies

This comprehensive specification covers all major features and technical aspects of the Physical AI & Humanoid Robotics educational platform, providing a complete reference for understanding, maintaining, and extending the system.