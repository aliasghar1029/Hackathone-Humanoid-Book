"""
Skills for translation tasks
"""
import asyncio
from typing import Dict, Any, List
import logging
import re

logger = logging.getLogger(__name__)

class TranslationSkills:
    """
    Reusable skills for translation tasks
    """

    @staticmethod
    async def preprocess_content_for_translation(content: str) -> str:
        """
        Preprocess content to make it more suitable for translation
        """
        try:
            # Remove excessive whitespace
            processed = re.sub(r'\s+', ' ', content.strip())

            # Handle special characters that might confuse the translation model
            processed = processed.replace('“', '"').replace('”', '"')
            processed = processed.replace('‘', "'").replace('’', "'")

            # Preserve code blocks or technical terms that shouldn't be translated
            # For now, we'll just return the processed content
            # In a real implementation, we'd identify and protect technical terms

            return processed

        except Exception as e:
            logger.error(f"Error preprocessing content for translation: {e}")
            return content.strip()

    @staticmethod
    async def identify_technical_terms(content: str) -> List[str]:
        """
        Identify technical terms that should be handled specially during translation
        """
        try:
            # Common technical terms in AI and robotics that might need special handling
            technical_terms = []

            # Patterns for technical terms
            patterns = [
                r'\b[A-Z]{2,}\b',  # Acronyms like AI, ML, CNN, RNN
                r'\b\w+ing\b',     # Technical gerunds like 'learning', 'processing'
                r'\b\w+ed\b',      # Technical past participles
                r'\b\w+ment\b',    # Technical nouns like 'movement', 'development'
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) > 2 and match not in technical_terms:  # Filter out short words
                        technical_terms.append(match)

            # Specific technical terms
            specific_terms = [
                'algorithm', 'neural network', 'machine learning', 'deep learning',
                'robotics', 'sensor', 'actuator', 'control system', 'feedback',
                'computer vision', 'path planning', 'kinematics', 'dynamics',
                'locomotion', 'manipulation', 'autonomy', 'navigation'
            ]

            for term in specific_terms:
                if term.lower() in content.lower() and term not in technical_terms:
                    technical_terms.append(term)

            return technical_terms

        except Exception as e:
            logger.error(f"Error identifying technical terms: {e}")
            return []

    @staticmethod
    async def validate_translation(translation: str, original: str) -> Dict[str, Any]:
        """
        Validate the quality and completeness of a translation
        """
        try:
            # Basic validation checks
            original_length = len(original.strip())
            translation_length = len(translation.strip())

            # Check if translation is too short compared to original (might be incomplete)
            length_ratio = translation_length / original_length if original_length > 0 else 0
            is_complete = length_ratio > 0.3  # At least 30% of original length

            # Check for common translation errors
            errors = []
            if "mock_urdu_translation" in translation:
                errors.append("Contains mock translation placeholder")
                is_complete = False

            # Check if translation contains original language (indicating incomplete translation)
            original_sample = original[:100].lower() if len(original) > 100 else original.lower()
            translation_sample = translation[:100].lower() if len(translation) > 100 else translation.lower()

            # Simple check for English words in translation (this is a basic check)
            original_english_words = set(original_sample.split()[:20])  # First 20 words
            translation_words = set(translation_sample.split()[:20])

            common_words = original_english_words.intersection(translation_words)
            if len(common_words) > len(original_english_words) * 0.5:  # More than 50% overlap
                errors.append("Translation contains too many original language words")

            return {
                "is_valid": len(errors) == 0 and is_complete,
                "is_complete": is_complete,
                "length_ratio": length_ratio,
                "errors": errors,
                "quality_score": min(1.0, length_ratio) if is_complete else 0.0
            }

        except Exception as e:
            logger.error(f"Error validating translation: {e}")
            return {
                "is_valid": False,
                "is_complete": False,
                "length_ratio": 0,
                "errors": [f"Validation error: {str(e)}"],
                "quality_score": 0.0
            }

    @staticmethod
    async def postprocess_translation(translation: str, original: str, target_language: str = "ur") -> str:
        """
        Postprocess translation to improve quality and consistency
        """
        try:
            processed = translation.strip()

            # Remove any placeholder text if present
            if "mock_urdu_translation:" in processed:
                # Extract the actual translation part
                parts = processed.split("mock_urdu_translation:", 1)
                if len(parts) > 1:
                    processed = parts[1].split("[", 1)[0].strip()  # Remove bracketed notes

            # Ensure proper formatting
            if target_language.lower() == "ur":
                # For Urdu, ensure right-to-left formatting if needed
                # For now, just clean up the text
                processed = re.sub(r'\s+', ' ', processed)  # Normalize whitespace

            return processed

        except Exception as e:
            logger.error(f"Error postprocessing translation: {e}")
            return translation.strip()

    @staticmethod
    async def get_translation_context(content_type: str, domain: str = "education") -> str:
        """
        Get appropriate context for translation based on content type and domain
        """
        try:
            base_context = f"Translate educational content in the {domain} domain."

            if content_type == "technical_code":
                context = f"{base_context} Preserve technical terminology and code structure. Translate explanations but keep technical terms in English if they are standard in the field."
            elif content_type == "theoretical":
                context = f"{base_context} Translate all concepts and explanations accurately while maintaining academic tone."
            elif content_type == "practical_example":
                context = f"{base_context} Translate examples and practical applications, maintaining clarity and applicability."
            elif content_type == "mathematical":
                context = f"{base_context} Translate mathematical explanations while preserving equations and formulas in their original form."
            elif content_type == "visual_description":
                context = f"{base_context} Translate descriptions of visual content accurately for comprehension."
            else:
                context = base_context

            return context

        except Exception as e:
            logger.error(f"Error getting translation context: {e}")
            return f"Translate educational content in the {domain} domain."

# Singleton instance
translation_skills = TranslationSkills()