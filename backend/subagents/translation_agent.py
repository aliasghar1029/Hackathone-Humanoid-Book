"""
Claude Subagent for translation functionality
"""
import asyncio
from typing import Dict, Any
import logging
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

class TranslationAgent:
    """
    Claude Subagent for handling content translation
    """

    def __init__(self):
        self.gemini_client = None
        try:
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if gemini_api_key and gemini_api_key.strip() != "":
                self.gemini_client = OpenAI(
                    api_key=gemini_api_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                logger.info("Translation agent initialized with Gemini client")
            else:
                logger.warning("GEMINI_API_KEY not set for translation agent")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client for translation agent: {e}")

    async def translate_content(self, content: str, target_language: str = "ur", context: str = None) -> str:
        """
        Translate content to target language using Claude/Gemini
        """
        try:
            if target_language.lower() != "ur":
                raise ValueError(f"Only Urdu translation is supported, got: {target_language}")

            if not content.strip():
                return content

            if self.gemini_client:
                # Create translation prompt with context
                prompt_context = context or "Educational content for Physical AI & Humanoid Robotics textbook"

                prompt = f"""
                Translate the following content to Urdu.
                Context: {prompt_context}

                Content to translate:
                {content[:3000]}  # Limit content to avoid token issues

                Please provide only the Urdu translation without any additional text or explanations.
                Preserve technical terminology and ensure the translation is accurate and readable.
                """

                response = self.gemini_client.chat.completions.create(
                    model="gemini-1.5-flash",
                    messages=[
                        {"role": "system", "content": "You are a professional translator specializing in technical and educational content. Translate accurately while preserving technical terminology and meaning. Respond only with the translated content in the target language."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=3000,
                    temperature=0.3
                )

                translated_content = response.choices[0].message.content.strip()
                return translated_content
            else:
                # Fallback to mock translation
                return f"mock_urdu_translation: {content[:100]}... [translated content in Urdu]"

        except Exception as e:
            logger.error(f"Translation error: {e}")
            # Return mock translation on error
            return f"mock_urdu_translation: {content[:100]}... [translation failed: {str(e)}]"

    async def batch_translate(self, contents: list, target_language: str = "ur", context: str = None) -> list:
        """
        Translate multiple content items
        """
        translations = []
        for content in contents:
            translation = await self.translate_content(content, target_language, context)
            translations.append(translation)
        return translations

# Singleton instance
translation_agent = TranslationAgent()