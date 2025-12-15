"""
Test script to validate all bonus features implementation
"""
import requests
import json
import time
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_authentication():
    """Test authentication system with background collection"""
    print("Testing Authentication System...")

    # Test signup with background
    signup_data = {
        "name": "Test User",
        "email": f"test{int(time.time())}@example.com",
        "password": "password123",
        "background": "software-focused",
        "preferences": {
            "hardware": "Laptop",
            "experience": "Intermediate",
            "language": "English"
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup",
                                headers=HEADERS, json=signup_data)
        print(f"Signup Response: {response.status_code}")
        print(f"Signup Data: {response.json()}")

        if response.status_code == 200:
            token = response.json().get('token')
            print("V Authentication system with background collection works")
            return token
        else:
            print(f"x Signup failed: {response.text}")
            return None
    except Exception as e:
        print(f"x Authentication test failed: {e}")
        return None

def test_personalization_api(token: str):
    """Test personalization API"""
    print("\nTesting Personalization API...")

    headers = {"Authorization": f"Bearer {token}", **HEADERS} if token else HEADERS

    # Test content personalization
    personalization_data = {
        "content": "This is a complex algorithm that requires both software implementation and hardware considerations.",
        "user_background": "software-focused",
        "preferences": {}
    }

    try:
        response = requests.post(f"{BASE_URL}/api/personalization/personalize-content",
                                headers=HEADERS, json=personalization_data)
        print(f"Personalization Response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Personalized Content: {result['personalized_content'][:100]}...")
            print("V Personalization API works")
            return True
        else:
            print(f"x Personalization failed: {response.text}")
            return False
    except Exception as e:
        print(f"x Personalization test failed: {e}")
        return False

def test_translation_api():
    """Test translation API"""
    print("\nTesting Translation API...")

    # Test translation to Urdu
    translation_data = {
        "content": "This is a test of the translation system for educational content.",
        "context": "Educational content for Physical AI & Humanoid Robotics textbook",
        "preserve_formatting": True
    }

    try:
        response = requests.post(f"{BASE_URL}/api/translate/to-urdu",
                                headers=HEADERS, json=translation_data)
        print(f"Translation Response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Translation Success: {result['success']}")
            print(f"Translated Content: {result['translated_content'][:100]}...")
            print("V Translation API works")
            return True
        else:
            print(f"x Translation failed: {response.text}")
            return False
    except Exception as e:
        print(f"x Translation test failed: {e}")
        return False

def test_subagents_api():
    """Test subagents functionality"""
    print("\nTesting Subagents API...")

    # Test content analysis
    analysis_data = {
        "content": "This is a technical explanation of neural networks and their implementation."
    }

    try:
        response = requests.post(f"{BASE_URL}/api/subagents/analyze-content",
                                headers=HEADERS, json=analysis_data)
        print(f"Subagent Analysis Response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Analysis Success: {result['success']}")
            print(f"Content Type: {result['result']['content_type']}")
            print("V Subagents API works")
            return True
        else:
            print(f"x Subagent analysis failed: {response.text}")
            return False
    except Exception as e:
        print(f"x Subagents test failed: {e}")
        return False

def test_integrated_query():
    """Test integrated query with personalization and translation"""
    print("\nTesting Integrated Query System...")

    # Test query with personalization and translation
    query_data = {
        "query": "Explain neural networks in robotics",
        "user_background": "software-focused",
        "target_language": "ur",
        "personalization_enabled": True,
        "translation_enabled": True
    }

    try:
        response = requests.post(f"{BASE_URL}/api/query",
                                headers=HEADERS, json=query_data)
        print(f"Integrated Query Response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Query Answer: {result['answer'][:100]}...")
            print(f"Personalization Applied: {result['personalization_applied']}")
            print(f"Translation Applied: {result['translation_applied']}")
            print("V Integrated query system works")
            return True
        else:
            print(f"x Integrated query failed: {response.text}")
            return False
    except Exception as e:
        print(f"x Integrated query test failed: {e}")
        return False

def test_health_checks():
    """Test health check endpoints"""
    print("\nTesting Health Checks...")

    endpoints_to_check = [
        "/api/health",
        "/api/auth/health",
        "/api/translate/health",
        "/api/subagents/health",
        "/api/personalization/health"
    ]

    all_healthy = True
    for endpoint in endpoints_to_check:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            status = response.json().get('status', 'unknown')
            print(f"{endpoint}: {status}")
            if status not in ['healthy', 'degraded']:  # degraded is acceptable
                all_healthy = False
        except Exception as e:
            print(f"x Health check for {endpoint} failed: {e}")
            all_healthy = False

    if all_healthy:
        print("V All services are healthy")
        return True
    else:
        print("x Some services are not healthy")
        return False

def main():
    """Run all tests"""
    print("Starting validation of bonus features...")
    print("="*50)

    # Test health checks first
    health_ok = test_health_checks()

    if not health_ok:
        print("\n! Some services are not healthy, but continuing with tests...")

    # Test authentication
    token = test_authentication()

    # Test personalization (with or without token)
    personalization_ok = test_personalization_api(token)

    # Test translation (doesn't require authentication)
    translation_ok = test_translation_api()

    # Test subagents
    subagents_ok = test_subagents_api()

    # Test integrated query
    integrated_ok = test_integrated_query()

    print("\n" + "="*50)
    print("VALIDATION SUMMARY:")
    print(f"Health Checks: {'V' if health_ok else 'x'}")
    print(f"Authentication: {'V' if token else 'x'}")
    print(f"Personalization: {'V' if personalization_ok else 'x'}")
    print(f"Translation: {'V' if translation_ok else 'x'}")
    print(f"Subagents: {'V' if subagents_ok else 'x'}")
    print(f"Integrated Query: {'V' if integrated_ok else 'x'}")

    all_tests_passed = all([health_ok, bool(token), personalization_ok, translation_ok, subagents_ok, integrated_ok])

    if all_tests_passed:
        print("\n*** All bonus features are working correctly!")
        return True
    else:
        print("\n!!! Some features need attention.")
        return False

if __name__ == "__main__":
    main()