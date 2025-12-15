from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import logging
from openai import OpenAI
import asyncio
import hashlib

import sys
import os
# Add the backend directory to the path to allow absolute imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from subagents.translation_agent import translation_agent
from skills.translation_skills import translation_skills

logger = logging.getLogger(__name__)

# Create router for translation endpoints
translation_router = APIRouter()

# Pydantic models for translation
class TranslationRequest(BaseModel):
    content: str
    context: Optional[str] = ""
    preserve_formatting: Optional[bool] = True

class TranslationResponse(BaseModel):
    original_content: str
    translated_content: str
    language: str
    success: bool
    cache_id: Optional[str] = None
    quality_score: Optional[float] = None

# Translation cache for performance optimization
translation_cache = {}

@translation_router.post("/to-urdu", response_model=TranslationResponse)
async def translate_to_urdu(request: TranslationRequest):
    """Translate content to Urdu with caching and quality validation"""
    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")

        # Create cache key based on content hash and context
        cache_key = hashlib.md5(f"{request.content}:{request.context}".encode()).hexdigest()

        # Check cache first
        if cache_key in translation_cache:
            cached_result = translation_cache[cache_key]
            logger.info(f"Translation served from cache with key: {cache_key}")
            return TranslationResponse(
                original_content=request.content,
                translated_content=cached_result,
                language="ur",
                success=True,
                cache_id=cache_key,
                quality_score=1.0  # Assume cached translations are high quality
            )

        # Preprocess content for translation
        processed_content = await translation_skills.preprocess_content_for_translation(request.content)

        # Get appropriate context for translation - temporarily use a default content type
        content_type = "general"  # Default content type
        translation_context = await translation_skills.get_translation_context(
            content_type=content_type,
            domain="education"
        )

        # Perform translation using the translation agent
        translated_content = await translation_agent.translate_content(
            content=processed_content,
            target_language="ur",
            context=translation_context
        )

        # Validate the translation quality
        validation = await translation_skills.validate_translation(translated_content, processed_content)

        # Postprocess the translation
        final_translation = await translation_skills.postprocess_translation(
            translated_content, processed_content, "ur"
        )

        # Cache the result if it's valid
        if validation["is_valid"]:
            translation_cache[cache_key] = final_translation

        return TranslationResponse(
            original_content=request.content,
            translated_content=final_translation,
            language="ur",
            success=validation["is_valid"],
            cache_id=cache_key if validation["is_valid"] else None,
            quality_score=validation["quality_score"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail="Translation service error")

@translation_router.get("/cache/{cache_id}")
async def get_cached_translation(cache_id: str):
    """Retrieve a cached translation"""
    try:
        if cache_id in translation_cache:
            return {
                "cache_id": cache_id,
                "translated_content": translation_cache[cache_id],
                "success": True
            }
        else:
            raise HTTPException(status_code=404, detail="Cached translation not found")
    except Exception as e:
        logger.error(f"Cache retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Cache retrieval error")

@translation_router.get("/health")
async def translation_health():
    """Health check for translation service"""
    try:
        # Check if Gemini client is available
        gemini_available = translation_agent.gemini_client is not None

        return {
            "status": "healthy" if gemini_available else "degraded",
            "services": {
                "translation_agent": {"status": "healthy" if gemini_available else "degraded (no Gemini)"},
                "translation_skills": {"status": "healthy"},
                "cache": {"status": "healthy", "size": len(translation_cache)}
            }
        }
    except Exception as e:
        logger.error(f"Translation health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# Add cache management endpoints
@translation_router.delete("/cache/clear")
async def clear_translation_cache():
    """Clear the translation cache"""
    global translation_cache
    count = len(translation_cache)
    translation_cache = {}
    return {"message": f"Cache cleared, {count} entries removed", "success": True}

@translation_router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(translation_cache),
        "status": "healthy"
    }