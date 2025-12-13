#!/usr/bin/env python3
"""
Test script for RAG Chatbot API endpoints
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_query_endpoint():
    """Test the query endpoint with a sample question"""
    print("\nTesting query endpoint...")
    try:
        payload = {
            "query": "What is humanoid robotics?",
            "selected_text": None
        }
        response = requests.post(f"{BASE_URL}/query", json=payload)
        print(f"Query endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Query response: {response.json()}")
        else:
            print(f"Query failed: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Query test failed: {e}")
        return False

def test_ingest_endpoint():
    """Test the ingest endpoint with sample content"""
    print("\nTesting ingest endpoint...")
    try:
        payload = {
            "file_path": "test_sample.md",
            "content": "# Test Document\nThis is a sample document for testing the RAG system.\n\nHumanoid robotics combines AI and mechanical engineering to create robots that mimic human behavior.",
            "metadata": {
                "title": "Test Document",
                "source": "test_sample.md",
                "page_number": 1
            }
        }
        response = requests.post(f"{BASE_URL}/ingest", json=payload)
        print(f"Ingest endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Ingest response: {response.json()}")
        else:
            print(f"Ingest failed: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Ingest test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting RAG Chatbot API tests...\n")

    # Check if required environment variables are set
    required_vars = ["QDRANT_URL", "QDRANT_API_KEY", "COHERE_API_KEY", "GEMINI_API_KEY", "DATABASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Missing required environment variables: {missing_vars}")
        print("Please set these variables in your .env file before running the tests.")
        exit(1)

    print("All required environment variables are present.")

    # Run tests
    health_ok = test_health_endpoint()
    query_ok = test_query_endpoint()
    ingest_ok = test_ingest_endpoint()

    print(f"\nTest Results:")
    print(f"Health endpoint: {'✓' if health_ok else '✗'}")
    print(f"Query endpoint: {'✓' if query_ok else '✗'}")
    print(f"Ingest endpoint: {'✓' if ingest_ok else '✗'}")

    if all([health_ok, query_ok, ingest_ok]):
        print("\nAll tests passed! ✅")
    else:
        print("\nSome tests failed! ❌")