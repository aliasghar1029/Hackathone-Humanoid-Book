"""
Advanced personalization logic based on user background
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import asyncio
import re

import sys
import os
# Add the backend directory to the path to allow absolute imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from subagents.personalization_agent import personalization_agent
from skills.personalization_skills import personalization_skills

logger = logging.getLogger(__name__)

# Create router for personalization endpoints
personalization_router = APIRouter()

# Pydantic models for personalization
class PersonalizationRequest(BaseModel):
    content: str
    user_background: str
    preferences: Optional[Dict[str, Any]] = None
    content_type: Optional[str] = "general"

class PersonalizationRule(BaseModel):
    id: str
    content_selector: str
    modification_type: str
    target_audience: List[str]
    modification_content: str
    priority: int

class PersonalizationResponse(BaseModel):
    original_content: str
    personalized_content: str
    applied_rules: List[str]
    content_analysis: Dict[str, Any]

@personalization_router.post("/personalize-content", response_model=PersonalizationResponse)
async def personalize_content(request: PersonalizationRequest):
    """Main endpoint to personalize content based on user background"""
    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")

        if not request.user_background:
            raise HTTPException(status_code=400, detail="User background is required")

        # Analyze the content first
        content_analysis = await personalization_skills.analyze_content_complexity(request.content)
        content_type = await personalization_skills.identify_content_type(request.content)
        key_concepts = await personalization_skills.extract_key_concepts(request.content)

        # Apply personalization using the agent
        personalized_content = await personalization_agent.personalize_content(
            content=request.content,
            user_background=request.user_background,
            preferences=request.preferences
        )

        # Additional personalization based on content type
        if content_type != "general":
            personalized_content = await personalization_skills.adapt_for_background(
                personalized_content,
                request.user_background,
                content_type
            )

        # Determine which rules were applied (for demo purposes)
        applied_rules = []
        if "software" in request.user_background.lower():
            applied_rules.append("software-focused enhancement")
        elif "hardware" in request.user_background.lower():
            applied_rules.append("hardware-focused enhancement")
        elif "mixed" in request.user_background.lower():
            applied_rules.append("mixed-background adaptation")
        elif "beginner" in request.user_background.lower():
            applied_rules.append("beginner-friendly simplification")

        response = PersonalizationResponse(
            original_content=request.content,
            personalized_content=personalized_content,
            applied_rules=applied_rules,
            content_analysis={
                "complexity": content_analysis,
                "content_type": content_type,
                "key_concepts": key_concepts
            }
        )

        logger.info(f"Content personalized for {request.user_background} background")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Personalization error: {e}")
        raise HTTPException(status_code=500, detail=f"Personalization failed: {str(e)}")

@personalization_router.post("/analyze-and-personalize", response_model=PersonalizationResponse)
async def analyze_and_personalize(request: PersonalizationRequest):
    """Analyze content and then personalize it"""
    try:
        # First, analyze the content
        analysis_result = await analyze_content_endpoint(ContentAnalysisRequest(content=request.content))

        # Then personalize based on the analysis
        content_analysis = analysis_result.result

        # Apply personalization
        personalized_content = await personalization_agent.personalize_content(
            content=request.content,
            user_background=request.user_background,
            preferences=request.preferences
        )

        # Additional adaptations based on analysis
        content_type = content_analysis.get("content_type", "general")
        if content_type != "general":
            personalized_content = await personalization_skills.adapt_for_background(
                personalized_content,
                request.user_background,
                content_type
            )

        # Determine applied rules
        applied_rules = []
        if content_analysis["complexity"]["complexity_level"] == "high":
            if "software" in request.user_background.lower():
                applied_rules.append("high-complexity software adaptation")
            elif "hardware" in request.user_background.lower():
                applied_rules.append("high-complexity hardware adaptation")
        elif content_analysis["complexity"]["complexity_level"] == "low":
            applied_rules.append("simplified adaptation for beginner level")

        response = PersonalizationResponse(
            original_content=request.content,
            personalized_content=personalized_content,
            applied_rules=applied_rules,
            content_analysis=content_analysis
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analyze and personalize error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis and personalization failed: {str(e)}")

@personalization_router.get("/user-profile-rules/{user_background}")
async def get_personalization_rules(user_background: str):
    """Get personalization rules for a specific user background"""
    try:
        # Define rules based on user background
        rules_map = {
            "software-focused": [
                {
                    "id": "sw_001",
                    "content_selector": "concept",
                    "modification_type": "technical_detail",
                    "target_audience": ["software-focused"],
                    "modification_content": "Implementation details and code examples",
                    "priority": 1
                },
                {
                    "id": "sw_002",
                    "content_selector": "system",
                    "modification_type": "architecture_focus",
                    "target_audience": ["software-focused"],
                    "modification_content": "Software architecture and design patterns",
                    "priority": 2
                }
            ],
            "hardware-focused": [
                {
                    "id": "hw_001",
                    "content_selector": "component",
                    "modification_type": "physical_detail",
                    "target_audience": ["hardware-focused"],
                    "modification_content": "Physical properties and electrical characteristics",
                    "priority": 1
                },
                {
                    "id": "hw_002",
                    "content_selector": "system",
                    "modification_type": "implementation_focus",
                    "target_audience": ["hardware-focused"],
                    "modification_content": "Hardware implementation and physical constraints",
                    "priority": 2
                }
            ],
            "mixed": [
                {
                    "id": "mx_001",
                    "content_selector": "concept",
                    "modification_type": "balanced_explanation",
                    "target_audience": ["mixed"],
                    "modification_content": "Both software and hardware perspectives",
                    "priority": 1
                },
                {
                    "id": "mx_002",
                    "content_selector": "system",
                    "modification_type": "integration_focus",
                    "target_audience": ["mixed"],
                    "modification_content": "Integration of software and hardware components",
                    "priority": 2
                }
            ],
            "beginner": [
                {
                    "id": "bg_001",
                    "content_selector": "complex_term",
                    "modification_type": "simplification",
                    "target_audience": ["beginner"],
                    "modification_content": "Simplified explanation of complex terms",
                    "priority": 1
                },
                {
                    "id": "bg_002",
                    "content_selector": "concept",
                    "modification_type": "foundational_focus",
                    "target_audience": ["beginner"],
                    "modification_content": "Focus on fundamental concepts before advanced details",
                    "priority": 2
                }
            ]
        }

        rules = rules_map.get(user_background, [])
        return {"user_background": user_background, "rules": rules}

    except Exception as e:
        logger.error(f"Get personalization rules error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get personalization rules: {str(e)}")

from pydantic import BaseModel

class ContentAnalysisRequest(BaseModel):
    content: str

async def analyze_content_endpoint(request: ContentAnalysisRequest):
    """Internal function to analyze content (used by other endpoints)"""
    try:
        # Analyze content complexity
        complexity = await personalization_skills.analyze_content_complexity(request.content)

        # Identify content type
        content_type = await personalization_skills.identify_content_type(request.content)

        # Extract key concepts
        key_concepts = await personalization_skills.extract_key_concepts(request.content)

        analysis_result = {
            "complexity": complexity,
            "content_type": content_type,
            "key_concepts": key_concepts
        }

        class MockResponse:
            def __init__(self, result):
                self.result = result

        return MockResponse(analysis_result)

    except Exception as e:
        logger.error(f"Content analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Content analysis failed: {str(e)}")

@personalization_router.get("/health")
async def personalization_health():
    """Health check for personalization service"""
    try:
        return {
            "status": "healthy",
            "services": {
                "personalization_agent": {"status": "available"},
                "personalization_skills": {"status": "available"}
            }
        }
    except Exception as e:
        logger.error(f"Personalization health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")