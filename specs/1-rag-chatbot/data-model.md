# Data Model: Integrated RAG Chatbot

## Entity: UserSession
- **Purpose**: Track user conversations with the chatbot
- **Fields**:
  - sessionId: UUID (primary key, required)
  - createdAt: DateTime (required, default: now)
  - lastActive: DateTime (required, default: now)
  - conversationHistory: JSON array of {query: string, response: string, timestamp: DateTime} (optional, max: 20 items)
  - selectedTextContext: String (optional, max: 10000 characters)

### Relationships
- One-to-many with ChatQuery (via sessionId foreign key)

### Constraints
- sessionId must be unique
- createdAt must be in the past
- lastActive must be >= createdAt
- conversationHistory limited to 20 most recent exchanges

## Entity: ContentChunk
- **Purpose**: Store indexed chunks of textbook content for RAG retrieval
- **Fields**:
  - chunkId: UUID (primary key, required)
  - content: Text (required, 50-2000 characters)
  - sourceDocument: String (required, e.g., "docs/intro.md")
  - section: String (optional, e.g., "Chapter 1.1")
  - pageNumber: Integer (optional)
  - metadata: JSON (optional, additional document metadata)
  - embeddingVector: Binary (required, vector representation for similarity search)
  - createdAt: DateTime (required, default: now)

### Relationships
- Many-to-many relationship with ChatQuery through sourcesUsed field

### Constraints
- content length: 50-2000 characters
- sourceDocument must exist in the textbook
- embeddingVector must be valid vector format
- createdAt must be in the past

## Entity: ChatQuery
- **Purpose**: Represent a user's query to the chatbot
- **Fields**:
  - queryId: UUID (primary key, required)
  - sessionId: UUID (foreign key to UserSession, required)
  - queryText: String (required, 1-1000 characters)
  - selectedText: String (optional, max: 1000 characters)
  - timestamp: DateTime (required, default: now)
  - sourcesUsed: Array of UUIDs (references to ContentChunk, optional)
  - responseId: UUID (foreign key to ChatResponse, optional)

### Relationships
- Belongs to UserSession (via sessionId)
- Has one ChatResponse (via responseId)
- References many ContentChunks (via sourcesUsed)

### Constraints
- queryText length: 1-1000 characters
  - sessionId must reference existing session
  - responseId must reference existing response (when present)
  - timestamp must be in the past

## Entity: ChatResponse
- **Purpose**: Store the chatbot's response to a user query
- **Fields**:
  - responseId: UUID (primary key, required)
  - queryId: UUID (foreign key to ChatQuery, required)
  - responseText: Text (required)
  - sources: JSON array of {title: string, source: string, page_number: integer, chunk_id: string, score: float} (optional)
  - confidenceLevel: Float (optional, 0.0-1.0, default: 0.8)
  - timestamp: DateTime (required, default: now)

### Relationships
- Belongs to ChatQuery (via queryId)

### Constraints
  - responseText must be provided
  - confidenceLevel must be between 0.0 and 1.0
  - timestamp must be in the past
  - sources array items must have valid structure

## Database Schema (PostgreSQL)

```sql
-- User sessions table
CREATE TABLE user_sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  last_active TIMESTAMP NOT NULL DEFAULT NOW(),
  conversation_history JSONB,
  selected_text_context TEXT
);

-- Content chunks table
CREATE TABLE content_chunks (
  chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  source_document VARCHAR(500) NOT NULL,
  section VARCHAR(200),
  page_number INTEGER,
  metadata JSONB,
  embedding_vector BYTEA NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for efficient content retrieval
CREATE INDEX idx_content_chunks_document ON content_chunks(source_document);
CREATE INDEX idx_content_chunks_section ON content_chunks(section);

-- Chat queries table
CREATE TABLE chat_queries (
  query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES user_sessions(session_id),
  query_text VARCHAR(1000) NOT NULL,
  selected_text TEXT,
  timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
  sources_used UUID[],
  response_id UUID REFERENCES chat_responses(response_id)
);

-- Index for efficient session queries
CREATE INDEX idx_chat_queries_session ON chat_queries(session_id);
CREATE INDEX idx_chat_queries_timestamp ON chat_queries(timestamp);

-- Chat responses table
CREATE TABLE chat_responses (
  response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query_id UUID NOT NULL UNIQUE REFERENCES chat_queries(query_id),
  response_text TEXT NOT NULL,
  sources JSONB,
  confidence_level DECIMAL(3,2) DEFAULT 0.80,
  timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for efficient query lookup
CREATE INDEX idx_chat_responses_query ON chat_responses(query_id);
```

## Vector Store Schema (Qdrant)

```yaml
collection_name: "textbook_content"
vectors_config:
  size: 1024  # Cohere embed-english-v3.0 returns 1024-dim vectors
  distance: "Cosine"

payload_schema:
  content:
    data_type: "text"
    indexes: true
  source_document:
    data_type: "keyword"
    indexes: true
  section:
    data_type: "keyword"
    indexes: true
  page_number:
    data_type: "integer"
    indexes: true
  metadata:
    data_type: "json"
    indexes: false
```

## Validation Rules

### UserSession Validation
- Session expiry: 24 hours of inactivity
- History trimming: Maintain only last 20 exchanges
- Session creation: Generate new session ID if none provided

### ContentChunk Validation
- Text chunking: Use semantic boundaries (sentences, paragraphs)
- Content deduplication: Prevent duplicate chunks
- Quality filtering: Remove low-value content chunks (headers, short fragments)

### ChatQuery Validation
- Input sanitization: Remove potential injection content
- Length limits: Enforce character limits
- Context preservation: Maintain conversation flow

### ChatResponse Validation
- Content safety: Filter inappropriate responses
- Source attribution: Verify cited content exists
- Confidence threshold: Flag low-confidence responses

## State Transitions

### UserSession States
- NEW: Session created but no queries yet
- ACTIVE: At least one query processed
- INACTIVE: No activity for extended period
- EXPIRED: Beyond 24-hour window

### ChatQuery States
- QUEUED: Query received, awaiting processing
- PROCESSING: RAG pipeline active
- COMPLETED: Response generated successfully
- FAILED: Processing error occurred

## Performance Considerations

### Indexing Strategy
- Database: Index session_id, timestamps, and source_document
- Vector Store: Enable HNSW indexing for efficient similarity search

### Caching Layers
- Content chunks: Cache frequently accessed content
- Embeddings: Cache computed embeddings to avoid recomputation
- Responses: Cache identical or similar queries

### Size Limits
- Content chunks: 50-2000 characters optimal for retrieval
- Session history: Limit to 20 exchanges for performance
- Metadata: Keep under 1KB per record