"""
API endpoints for Claude Subagents
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import asyncio

import sys
import os
# Add the backend directory to the path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from subagents.personalization_agent import personalization_agent
from subagents.translation_agent import translation_agent
from skills.personalization_skills import personalization_skills
from skills.translation_skills import translation_skills

logger = logging.getLogger(__name__)

# Create router for subagent endpoints
subagent_router = APIRouter()

# Pydantic models for subagent API
class PersonalizationRequest(BaseModel):
    content: str
    user_background: str
    preferences: Optional[Dict[str, Any]] = None

class TranslationRequest(BaseModel):
    content: str
    target_language: str = "ur"
    context: Optional[str] = None

class ContentAnalysisRequest(BaseModel):
    content: str

class SubagentResponse(BaseModel):
    success: bool
    result: Any
    message: Optional[str] = None

@subagent_router.post("/personalize", response_model=SubagentResponse)
async def personalize_content_endpoint(request: PersonalizationRequest):
    """Endpoint to personalize content based on user background"""
    try:
        personalized_content = await personalization_agent.personalize_content(
            content=request.content,
            user_background=request.user_background,
            preferences=request.preferences
        )

        return SubagentResponse(
            success=True,
            result=personalized_content,
            message="Content personalized successfully"
        )
    except Exception as e:
        logger.error(f"Personalization error: {e}")
        raise HTTPException(status_code=500, detail=f"Personalization failed: {str(e)}")

@subagent_router.post("/translate", response_model=SubagentResponse)
async def translate_content_endpoint(request: TranslationRequest):
    """Endpoint to translate content to target language"""
    try:
        translated_content = await translation_agent.translate_content(
            content=request.content,
            target_language=request.target_language,
            context=request.context
        )

        # Validate the translation
        validation = await translation_skills.validate_translation(
            translated_content, request.content
        )

        if not validation["is_valid"]:
            logger.warning(f"Translation validation issues: {validation['errors']}")

        # Postprocess the translation
        final_translation = await translation_skills.postprocess_translation(
            translated_content, request.content, request.target_language
        )

        return SubagentResponse(
            success=True,
            result=final_translation,
            message="Content translated successfully"
        )
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@subagent_router.post("/analyze-content", response_model=SubagentResponse)
async def analyze_content_endpoint(request: ContentAnalysisRequest):
    """Endpoint to analyze content for personalization"""
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

        return SubagentResponse(
            success=True,
            result=analysis_result,
            message="Content analysis completed successfully"
        )
    except Exception as e:
        logger.error(f"Content analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Content analysis failed: {str(e)}")

@subagent_router.post("/adapt-for-user", response_model=SubagentResponse)
async def adapt_content_for_user_endpoint(request: PersonalizationRequest):
    """Endpoint to adapt content specifically for a user's background"""
    try:
        # First analyze the content
        content_type = await personalization_skills.identify_content_type(request.content)

        # Adapt the content based on user background and content type
        adapted_content = await personalization_skills.adapt_for_background(
            request.content,
            request.user_background,
            content_type
        )

        return SubagentResponse(
            success=True,
            result=adapted_content,
            message="Content adapted for user successfully"
        )
    except Exception as e:
        logger.error(f"Content adaptation error: {e}")
        raise HTTPException(status_code=500, detail=f"Content adaptation failed: {str(e)}")

@subagent_router.get("/health")
async def subagent_health():
    """Health check for subagent services"""
    try:
        # Check if Gemini clients are available
        gemini_available = translation_agent.gemini_client is not None

        return {
            "status": "healthy" if gemini_available else "degraded",
            "services": {
                "personalization_agent": {"status": "healthy"},
                "translation_agent": {"status": "healthy" if gemini_available else "degraded (no Gemini)"},
                "skills": {"status": "healthy"}
            }
        }
    except Exception as e:
        logger.error(f"Subagent health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")