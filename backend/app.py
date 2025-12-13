import os
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv
import uuid
from datetime import datetime
import logging
import json
import re
import time


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Add custom middleware for timeout handling
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        # Log the exception and return a timeout response if needed
        process_time = time.time() - start_time
        logger.error(f"Request failed after {process_time:.2f}s: {e}")
        raise e

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Add CORS middleware to allow requests from Docusaurus (with proxy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://aliasghar1029.github.io", "http://localhost:3001", "http://0.0.0.0:3000"],  # Allow specific origins including additional common ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
try:
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL or QDRANT_API_KEY environment variables not set")

    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=False
    )
    logger.info("Qdrant client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Qdrant client: {e}")
    qdrant_client = None

try:
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key or cohere_api_key.strip() == "":
        raise ValueError("COHERE_API_KEY is missing or empty")

    co = cohere.Client(api_key=cohere_api_key, timeout=30)  # 30 second timeout for API calls
    logger.info("Cohere client initialized successfully with timeout configuration")
except Exception as e:
    logger.error(f"Failed to initialize Cohere client: {e}")
    co = None

# Initialize OpenAI client with Gemini - FIXED: Removed proxies argument and added proper error handling
# try:
#     gemini_api_key = os.getenv("GEMINI_API_KEY")
#     if not gemini_api_key:
#         raise ValueError("GEMINI_API_KEY environment variable not set")

#     client = OpenAI(
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#         api_key=gemini_api_key
#     )
#     logger.info("OpenAI (Gemini) client initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize OpenAI (Gemini) client: {e}")
#     client = None
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key or gemini_api_key.strip() == "":
        raise ValueError("GEMINI_API_KEY is missing or empty")

    # Initialize OpenAI client with Gemini API - with extended timeout configuration
    client = OpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        timeout=60.0  # 60 second timeout for API calls to handle longer responses
    )
    logger.info("OpenAI (Gemini) client initialized successfully with extended timeout configuration")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI (Gemini) client: {e}")
    client = None
# Database connection
def get_db_connection():
    try:
        return psycopg2.connect(os.getenv("DATABASE_URL"))
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str  # Changed from 'response' to 'answer' to match frontend expectation
    sources: Optional[List[Dict[str, Any]]] = []

class IngestRequest(BaseModel):
    file_path: str
    content: str
    metadata: Dict[str, Any]


# Initialize collections
def init_collections():
    if not qdrant_client:
        logger.error("Qdrant client not available, skipping collection initialization")
        return

    try:
        # Check if collection exists, if not create it
        qdrant_client.get_collection("documents")
        logger.info("Documents collection exists")
    except:
        try:
            # Create collection for document chunks
            qdrant_client.create_collection(
                collection_name="documents",
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),  # Cohere embed-english-v3.0 returns 1024-dim vectors
            )
            logger.info("Documents collection created successfully")
        except Exception as e:
            logger.error(f"Failed to create documents collection: {e}")

# Initialize on startup
@app.on_event("startup")
def startup_event():
    init_collections()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    try:
        logger.info(f"Received query: {request.query[:100]}...")
        if request.selected_text:
            logger.info(f"Received selected text: {request.selected_text[:100]}...")

        # Validate clients - FIXED: Check for None values properly
        if not qdrant_client:
            error_msg = "Qdrant client not initialized. Please check QDRANT_URL and QDRANT_API_KEY environment variables."
            logger.error(error_msg)
            return QueryResponse(answer=error_msg, sources=[])

        if not co:
            error_msg = "Cohere client not initialized. Please check COHERE_API_KEY environment variable."
            logger.error(error_msg)
            return QueryResponse(answer=error_msg, sources=[])

        if not client:
            error_msg = "Gemini client not initialized. Please check GEMINI_API_KEY environment variable."
            logger.error(error_msg)
            return QueryResponse(answer=error_msg, sources=[])

        # Sanitize inputs to handle special characters and newlines
        query = request.query.strip() if request.query else ""
        selected_text = request.selected_text.strip() if request.selected_text else ""

        if not query:
            return QueryResponse(answer="Please provide a query.", sources=[])

        # Generate embedding for the query with timeout
        query_embedding = None
        try:
            query_embedding = co.embed(
                texts=[query],
                model='embed-english-v3.0',
                input_type="search_query"
            ).embeddings[0]
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            return QueryResponse(answer="Failed to process your query. Please try again.", sources=[])

        # Prepare search conditions
        search_results = []

        # If selected text exists, prioritize it
        if selected_text:
            try:
                # First, search specifically for chunks related to the selected text
                selected_text_embedding = None
                try:
                    selected_text_embedding = co.embed(
                        texts=[selected_text],
                        model='embed-english-v3.0',
                        input_type="search_query"
                    ).embeddings[0]
                except Exception as e:
                    logger.error(f"Failed to generate selected text embedding: {e}")

                if selected_text_embedding:
                    # Search for similar chunks to the selected text
                    selected_results = qdrant_client.search(
                        collection_name="documents",
                        query_vector=selected_text_embedding,
                        limit=2,  # Reduced limit for faster response
                        with_payload=True,
                        with_vectors=False
                    )

                    # Also search for general query
                    general_results = qdrant_client.search(
                        collection_name="documents",
                        query_vector=query_embedding,
                        limit=3,  # Reduced limit for faster response
                        with_payload=True,
                        with_vectors=False
                    )

                    # Combine results, prioritizing those related to selected text
                    all_results = selected_results + [r for r in general_results if r not in selected_results]
                    search_results = all_results[:5]  # Limit to 5 total results for faster response
                else:
                    # Fallback to general search only
                    search_results = qdrant_client.search(
                        collection_name="documents",
                        query_vector=query_embedding,
                        limit=5,  # Reduced limit for faster response
                        with_payload=True,
                        with_vectors=False
                    )
            except Exception as e:
                logger.error(f"Error during search with selected text: {e}")
                # Fallback to general search only
                try:
                    search_results = qdrant_client.search(
                        collection_name="documents",
                        query_vector=query_embedding,
                        limit=5,  # Reduced limit for faster response
                        with_payload=True,
                        with_vectors=False
                    )
                except Exception as e2:
                    logger.error(f"Fallback search also failed: {e2}")
                    return QueryResponse(answer="Search service is temporarily unavailable. Please try again later.", sources=[])
        else:
            # Just search for the query
            try:
                search_results = qdrant_client.search(
                    collection_name="documents",
                    query_vector=query_embedding,
                    limit=5,  # Reduced limit for faster response
                    with_payload=True,
                    with_vectors=False
                )
            except Exception as e:
                logger.error(f"General search failed: {e}")
                return QueryResponse(answer="Search service is temporarily unavailable. Please try again later.", sources=[])

        # Extract content and metadata from results
        context_parts = []
        sources = []

        for result in search_results:
            try:
                payload = result.payload
                content = payload.get("content", "")
                metadata = payload.get("metadata", {})

                if content.strip():  # Only add non-empty content
                    context_parts.append(content)

                sources.append({
                    "title": metadata.get("title", ""),
                    "source": metadata.get("source", ""),
                    "page_number": metadata.get("page_number", 0),
                    "chunk_id": metadata.get("chunk_id", ""),
                    "score": result.score
                })
            except Exception as e:
                logger.error(f"Error processing search result: {e}")
                continue

        # Build context for LLM - limit context to avoid token limits
        context = "\n\n".join(context_parts[:3])  # Use only first 3 chunks for faster processing

        # Limit context length to prevent exceeding model limits
        if len(context) > 2000:  # Reduced limit for faster processing
            context = context[:2000] + "... (truncated)"

        # Build the prompt for the LLM
        if selected_text:
            prompt = f"""
You are an expert assistant for the Physical AI & Humanoid Robotics Textbook. Answer the user's question based on the provided context.

IMPORTANT: The user has selected specific text that they want to focus on. Prioritize answering about this selected text in your response.

Selected Text: {selected_text}

Context from the textbook:
{context}

Question: {request.query}

Please provide a detailed answer based on the context, with special focus on the selected text if relevant.
"""
        else:
            prompt = f"""
You are an expert assistant for the Physical AI & Humanoid Robotics Textbook. Answer the user's question based on the provided context.

Context from the textbook:
{context}

Question: {request.query}

Please provide a detailed answer based on the context.
"""

        # Generate response using Gemini with additional timeout handling
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are an expert assistant for the Physical AI & Humanoid Robotics Textbook. Provide accurate, helpful answers based on the context provided. Be concise but thorough, and cite relevant information from the textbook when possible."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,  # Reduced for faster response
            temperature=0.7,
            timeout=45.0  # Reduced timeout for faster failover
        )

        answer = response.choices[0].message.content
        process_time = time.time() - start_time
        logger.info(f"Query processed in {process_time:.2f}s")

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error in query_endpoint after {process_time:.2f}s: {e}", exc_info=True)
        return QueryResponse(answer="I'm having trouble generating a response right now. The server might be busy. Please try again in a moment.", sources=[])

        # Prepare search conditions
        search_results = []

        # If selected text exists, prioritize it
        if selected_text:
            try:
                # First, search specifically for chunks related to the selected text
                selected_text_embedding = co.embed(
                    texts=[selected_text],
                    model='embed-english-v3.0',
                    input_type="search_query"
                ).embeddings[0]

                # Search for similar chunks to the selected text
                selected_results = qdrant_client.search(
                    collection_name="documents",
                    query_vector=selected_text_embedding,
                    limit=3,
                    with_payload=True,
                    with_vectors=False
                )

                # Also search for general query
                general_results = qdrant_client.search(
                    collection_name="documents",
                    query_vector=query_embedding,
                    limit=5,
                    with_payload=True,
                    with_vectors=False
                )

                # Combine results, prioritizing those related to selected text
                all_results = selected_results + [r for r in general_results if r not in selected_results]
                search_results = all_results[:8]  # Limit to 8 total results
            except Exception as e:
                logger.error(f"Error during search with selected text: {e}")
                # Fallback to general search only
                try:
                    search_results = qdrant_client.search(
                        collection_name="documents",
                        query_vector=query_embedding,
                        limit=8,
                        with_payload=True,
                        with_vectors=False
                    )
                except Exception as e2:
                    logger.error(f"Fallback search also failed: {e2}")
                    return QueryResponse(answer="Search service is temporarily unavailable. Please try again later.", sources=[])
        else:
            # Just search for the query
            try:
                search_results = qdrant_client.search(
                    collection_name="documents",
                    query_vector=query_embedding,
                    limit=8,
                    with_payload=True,
                    with_vectors=False
                )
            except Exception as e:
                logger.error(f"General search failed: {e}")
                return QueryResponse(answer="Search service is temporarily unavailable. Please try again later.", sources=[])

        # Extract content and metadata from results
        context_parts = []
        sources = []

        for result in search_results:
            try:
                payload = result.payload
                content = payload.get("content", "")
                metadata = payload.get("metadata", {})

                if content.strip():  # Only add non-empty content
                    context_parts.append(content)

                sources.append({
                    "title": metadata.get("title", ""),
                    "source": metadata.get("source", ""),
                    "page_number": metadata.get("page_number", 0),
                    "chunk_id": metadata.get("chunk_id", ""),
                    "score": result.score
                })
            except Exception as e:
                logger.error(f"Error processing search result: {e}")
                continue

        # Build context for LLM - limit context to avoid token limits
        context = "\n\n".join(context_parts[:5])  # Use only first 5 chunks to avoid token limits

        # Limit context length to prevent exceeding model limits
        if len(context) > 3000:  # Rough limit to stay within token limits
            context = context[:3000] + "... (truncated)"

        # Build the prompt for the LLM
        if selected_text:
            prompt = f"""
You are an expert assistant for the Physical AI & Humanoid Robotics Textbook. Answer the user's question based on the provided context.

IMPORTANT: The user has selected specific text that they want to focus on. Prioritize answering about this selected text in your response.

Selected Text: {selected_text}

Context from the textbook:
{context}

Question: {request.query}

Please provide a detailed answer based on the context, with special focus on the selected text if relevant.
"""
        else:
            prompt = f"""
You are an expert assistant for the Physical AI & Humanoid Robotics Textbook. Answer the user's question based on the provided context.

Context from the textbook:
{context}

Question: {request.query}

Please provide a detailed answer based on the context.
"""

        try:
            # Generate response using Gemini with additional timeout handling
            response = client.chat.completions.create(
                model="gemini-1.5-flash",
                messages=[
                    {"role": "system", "content": "You are an expert assistant for the Physical AI & Humanoid Robotics Textbook. Provide accurate, helpful answers based on the context provided. Be concise but thorough, and cite relevant information from the textbook when possible."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
                timeout=50.0  # Additional timeout for the completion request
            )

            answer = response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Provide a more specific error message for timeout-related issues
            if "timeout" in str(e).lower() or "504" in str(e):
                return QueryResponse(answer="The response is taking longer than expected. Please try your question again in a moment.", sources=sources)
            else:
                return QueryResponse(answer="I'm having trouble generating a response right now. Please try again later.", sources=sources)

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        logger.error(f"Unexpected error in query_endpoint: {e}", exc_info=True)
        return QueryResponse(answer="An unexpected error occurred. Please try again later.", sources=[])

@app.post("/ingest")
async def ingest_document(request: IngestRequest, background_tasks: BackgroundTasks):
    try:
        # Process the document in the background
        background_tasks.add_task(process_and_store_document, request.file_path, request.content, request.metadata)
        return {"message": "Document ingestion started", "file_path": request.file_path}
    except Exception as e:
        logger.error(f"Error starting ingestion: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting ingestion: {str(e)}")

def process_and_store_document(file_path: str, content: str, metadata: Dict[str, Any]):
    """Process and store document in Qdrant and database"""
    try:
        # Simple chunking (you might want to use more sophisticated methods)
        chunks = chunk_text(content)

        points = []
        for i, chunk in enumerate(chunks):
            try:
                # Generate embedding for the chunk
                embedding = co.embed(
                    texts=[chunk],
                    model='embed-english-v3.0',
                    input_type="search_document"
                ).embeddings[0]

                # Create a point for Qdrant
                point = models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "content": chunk,
                        "metadata": {
                            "title": metadata.get("title", ""),
                            "source": file_path,
                            "page_number": metadata.get("page_number", 0),
                            "chunk_id": f"{file_path}_chunk_{i}",
                            "created_at": datetime.utcnow().isoformat()
                        }
                    }
                )
                points.append(point)
            except Exception as e:
                logger.error(f"Error processing chunk {i} for {file_path}: {e}")
                continue

        # Upload points to Qdrant
        if points:
            qdrant_client.upsert(
                collection_name="documents",
                points=points
            )

        # Store metadata in PostgreSQL (optional, for additional metadata tracking)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()

            # Create table if it doesn't exist (in a real app, you'd handle this with migrations)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Insert document metadata
            cursor.execute(
                "INSERT INTO documents (file_path, title) VALUES (%s, %s)",
                (file_path, metadata.get("title", ""))
            )

            conn.commit()
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"Error processing document {file_path}: {e}")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Simple text chunking function"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're near the end, just take the rest
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Try to break at sentence boundary
        chunk = text[start:end]

        # Find the last sentence ending in the chunk
        sentence_endings = [chunk.rfind('. '), chunk.rfind('? '), chunk.rfind('! '), chunk.rfind('\n')]
        sentence_end = max(sentence_endings)

        if sentence_end > len(chunk) // 2:  # If sentence ending is in the second half
            end = start + sentence_end + 2
            chunk = text[start:end]

        chunks.append(chunk)
        start = end - overlap  # Overlap to maintain context

    # Filter out empty chunks
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks

@app.get("/health")
async def health_check():
    """Health check endpoint to verify all services are running"""
    qdrant_status = False
    cohere_status = False
    gemini_status = False
    db_status = False

    # Check Qdrant connection
    try:
        if qdrant_client:
            qdrant_client.get_collection("documents")
            qdrant_status = True
    except:
        pass

    # Check Cohere connection
    try:
        if co:
            # Simple test to verify Cohere client works
            co.check_api_key()
            cohere_status = True
    except:
        pass

    # Check Gemini connection
    try:
        if client:
            # Simple test to verify Gemini client works
            client.models.list()
            gemini_status = True
    except:
        pass

    # Check database connection
    try:
        if get_db_connection():
            db_status = True
    except:
        pass

    status = "healthy" if all([qdrant_status, cohere_status, gemini_status]) else "unhealthy"

    return {
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "qdrant": {"status": "healthy" if qdrant_status else "unhealthy"},
            "cohere": {"status": "healthy" if cohere_status else "unhealthy"},
            "gemini": {"status": "healthy" if gemini_status else "unhealthy"},
            "database": {"status": "healthy" if db_status else "unhealthy"}
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)