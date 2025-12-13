# Technical Implementation Plan: Integrated RAG Chatbot

## Technical Context

**Feature**: Integrated RAG Chatbot Development
**Domain**: Educational Docusaurus textbook with intelligent Q&A
**Architecture**: FastAPI backend, Neon Postgres, Qdrant vector store, OpenAI Agents/ChatKit for RAG
**Integration**: Embedded chatbot widget in Docusaurus book pages

### Technology Stack
- **Frontend**: Docusaurus v3 with React components
- **Backend**: FastAPI API server
- **Database**: Neon Serverless Postgres
- **Vector Store**: Qdrant Cloud Free Tier
- **AI Processing**: OpenAI Agents/ChatKit SDKs
- **Text Processing**: Cohere embeddings for vectorization
- **Infrastructure**: Containerized deployment with Docker

### Unknowns & Dependencies
- Textbook content structure and format for ingestion
- Specific OpenAI Agents/ChatKit SDK integration patterns
- MCP context7 integration methodology
- Rate limiting and cost considerations for API usage
- Security requirements for user sessions and data privacy

## Constitution Check

### Alignment with Core Principles

#### I. Deliverable Focus
- ✅ RAG chatbot enhances the primary Docusaurus site deliverable
- ✅ Implementation supports the core goal of providing textbook content accessibly
- ✅ All development aligns with enhancing the Docusaurus site experience

#### II. Content Fidelity & Presentation
- ✅ Chatbot responses will be grounded in exact textbook content
- ✅ Responses will maintain professional presentation standards
- ✅ Citations will preserve content integrity and attribution

#### III. User Experience & Accessibility
- ✅ Mobile-responsive chatbot interface planned
- ✅ Integration designed for seamless user experience
- ✅ Accessibility features included in design

#### IV. Technical Architecture & Extensibility
- ✅ RAG architecture inherently supports the extensibility principle
- ✅ Clean data models planned for content indexing
- ✅ API-first design enables future enhancements

#### V. Hackathon Compliance
- ✅ Implementation follows established project patterns
- ✅ Architecture supports base requirements while adding premium features

### Potential Violations
No constitutional violations identified. The RAG chatbot directly supports Principle IV (Technical Architecture & Extensibility).

## Research Phase

### RQ-1: Textbook Content Ingestion Strategy
**Decision**: Use MDX content extraction with chunking for RAG indexing
**Rationale**: Docusaurus MDX files can be programmatically extracted and converted to vector embeddings for retrieval
**Alternatives considered**:
- Direct PDF parsing (complex, less accurate)
- Manual content conversion (time-intensive, error-prone)
- API-based content extraction (most flexible and maintainable)

### RQ-2: OpenAI Agents vs ChatKit SDK Selection
**Decision**: Use OpenAI-compatible API with Cohere embeddings for cost-effective processing
**Rationale**: OpenAI-compatible APIs (like Google's Gemini API) provide better cost/performance for educational use
**Alternatives considered**:
- Native OpenAI SDK (higher costs for educational project)
- OpenAI Agents framework (potentially overengineered for RAG)
- Cohere API directly (already integrated in existing codebase)

### RQ-3: Session Management Approach
**Decision**: Implement JWT-based session management with in-memory caching
**Rationale**: JWTs provide stateless authentication while enabling conversation context preservation
**Alternatives considered**:
- Cookie-based sessions (more complex with proxy setup)
- Server-side session storage (increases backend complexity)
- Local storage only (security concerns, limited context)

### RQ-4: MCP Context7 Integration
**Decision**: Create MCP-compatible documentation adapter for real-time content updates
**Rationale**: MCP context7 provides latest documentation which can enhance RAG responses
**Implementation**: Adapter layer will fetch from context7 when available and fall back to static content

## Phase 1: Data Model Design

### Entity: UserSession
- **Fields**:
  - sessionId: UUID (primary key)
  - createdAt: DateTime
  - lastActive: DateTime
  - conversationHistory: JSON array of query-response pairs
  - selectedTextContext: String (optional)
- **Relationships**: None
- **Validation**:
  - sessionId must be unique
  - createdAt must be in past
  - conversationHistory limited to 20 entries
- **State transitions**: Active → Expired (after 24 hours of inactivity)

### Entity: ContentChunk
- **Fields**:
  - chunkId: UUID (primary key)
  - content: Text (the actual content chunk)
  - sourceDocument: String (filename or URL)
  - section: String (chapter/section reference)
  - pageNumber: Integer (optional)
  - metadata: JSON (additional document metadata)
  - embeddingVector: Binary (vector representation for similarity search)
- **Relationships**: None
- **Validation**:
  - content must be 50-2000 characters
  - sourceDocument must exist
  - embeddingVector must be valid vector format
- **State transitions**: None

### Entity: ChatQuery
- **Fields**:
  - queryId: UUID (primary key)
  - sessionId: UUID (foreign key to UserSession)
  - queryText: String
  - selectedText: String (optional)
  - timestamp: DateTime
  - sourcesUsed: Array of UUIDs (referencing ContentChunk)
  - responseId: UUID (foreign key to ChatResponse)
- **Relationships**:
  - Belongs to UserSession
  - Has one ChatResponse
  - References multiple ContentChunks
- **Validation**:
  - queryText must be 1-1000 characters
  - sessionId must reference existing session
- **State transitions**: Queued → Processing → Completed/Failed

### Entity: ChatResponse
- **Fields**:
  - responseId: UUID (primary key)
  - queryId: UUID (foreign key to ChatQuery)
  - responseText: Text
  - sources: JSON array of source citations
  - confidenceLevel: Float (0.0-1.0)
  - timestamp: DateTime
- **Relationships**:
  - Belongs to ChatQuery
- **Validation**:
  - responseText must be provided
  - confidenceLevel must be between 0.0 and 1.0
- **State transitions**: None (responses are immutable once created)

## Phase 1: API Contract Design

### Endpoint: POST /api/chat/query
**Purpose**: Process user query and return RAG-enhanced response
**Request**:
```json
{
  "query": "string (required)",
  "selected_text": "string (optional)",
  "session_id": "string (optional)"
}
```
**Response**:
```json
{
  "response": "string",
  "sources": [
    {
      "title": "string",
      "source": "string",
      "page_number": "integer",
      "chunk_id": "string",
      "score": "float"
    }
  ],
  "session_id": "string",
  "confidence": "float"
}
```
**Status Codes**:
- 200: Successful response
- 400: Invalid request format
- 429: Rate limit exceeded
- 500: Processing error

### Endpoint: GET /api/chat/session/{sessionId}
**Purpose**: Retrieve conversation history for a session
**Response**:
```json
{
  "session_id": "string",
  "history": [
    {
      "query": "string",
      "response": "string",
      "timestamp": "datetime"
    }
  ]
}
```
**Status Codes**:
- 200: Successful retrieval
- 404: Session not found
- 500: Database error

### Endpoint: POST /api/content/ingest
**Purpose**: Ingest textbook content into the RAG system
**Request**:
```json
{
  "file_path": "string",
  "content": "string",
  "metadata": {
    "title": "string",
    "source": "string",
    "page_number": "integer"
  }
}
```
**Response**:
```json
{
  "message": "string",
  "chunks_processed": "integer"
}
```
**Status Codes**:
- 200: Ingestion started successfully
- 400: Invalid content format
- 500: Ingestion error

## Phase 1: Infrastructure Design

### FastAPI Application Structure
```
backend/
├── app.py                 # Main FastAPI application
├── models.py             # Pydantic models and database models
├── database.py           # Database connection and setup
├── vector_store.py       # Qdrant client and operations
├── rag_engine.py         # RAG logic and processing
├── auth.py               # Authentication utilities
└── routes/
    ├── chat.py           # Chat API endpoints
    ├── content.py        # Content ingestion endpoints
    └── session.py        # Session management endpoints
```

### Frontend Integration
```
src/
├── components/
│   ├── ChatbotWidget.jsx    # Main chatbot UI component
│   ├── ChatInterface.jsx    # Chat interface with message history
│   └── ContentSelector.jsx  # Handles selected text context
├── css/
│   └── chatbot.css         # Chatbot styling
└── plugins/
    └── proxyPlugin.js      # Development proxy for API calls
```

### Data Pipeline
1. **Content Extraction**: Extract MDX content from Docusaurus docs
2. **Text Chunking**: Split content into searchable chunks
3. **Embedding Generation**: Create vector embeddings using Cohere
4. **Vector Storage**: Store embeddings in Qdrant with metadata
5. **Query Processing**: Match user queries to relevant content chunks
6. **Response Generation**: Create contextual responses with citations

## Phase 1: Security Considerations

### Authentication & Authorization
- JWT tokens for session management
- Rate limiting per IP/session
- Input sanitization for all user queries
- Secure storage of API keys in environment variables

### Data Privacy
- No PII collection
- Session data purged after 24 hours
- Query/response logs anonymized
- Content indexing only from approved textbook materials

### API Security
- CORS configured for Docusaurus domain only
- Input validation on all endpoints
- SQL injection protection via parameterized queries
- XSS prevention through output encoding

## Phase 1: Performance Optimization

### Caching Strategy
- Content chunk caching in Redis/Memory
- Embedding result caching
- Session state caching
- CDN for static assets

### Scalability Considerations
- Stateless API design for horizontal scaling
- Connection pooling for database
- Async processing for long-running operations
- Queue system for content ingestion jobs

### Monitoring & Logging
- Structured logging for debugging
- Performance metrics collection
- Error tracking and alerting
- Usage analytics for optimization

## Implementation Roadmap

### Milestone 1: Foundation Setup
- [ ] FastAPI backend with basic routing
- [ ] Neon Postgres connection and models
- [ ] Qdrant vector store setup and client
- [ ] Basic chat endpoint with mock responses

### Milestone 2: RAG Engine
- [ ] Content ingestion pipeline
- [ ] Embedding generation and storage
- [ ] Similarity search implementation
- [ ] Response generation with citations

### Milestone 3: Frontend Integration
- [ ] Chatbot widget UI component
- [ ] Selected text context handling
- [ ] Session management in browser
- [ ] API integration and error handling

### Milestone 4: Enhancement & Testing
- [ ] MCP context7 integration
- [ ] Performance optimization
- [ ] Security hardening
- [ ] User testing and feedback incorporation

## Success Criteria Verification

### Quantitative Measures
- Response time: <5 seconds for 95% of queries
- Content accuracy: >90% factual correctness
- System availability: >99% uptime
- Concurrent user support: >100 users simultaneously

### Qualitative Measures
- Seamless integration with Docusaurus reading experience
- Natural, helpful conversation flow
- Accurate source attribution
- Mobile-responsive design

## Risk Analysis

### High Priority Risks
- API rate limits affecting response time
- Vector store costs exceeding free tier limits
- Content quality issues in responses

### Mitigation Strategies
- Implement caching to reduce API calls
- Monitor usage and optimize embedding efficiency
- Include human validation in content pipeline