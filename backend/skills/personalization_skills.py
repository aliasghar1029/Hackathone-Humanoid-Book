"""
Skills for personalization tasks
"""
import asyncio
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class PersonalizationSkills:
    """
    Reusable skills for personalization tasks
    """

    @staticmethod
    async def analyze_content_complexity(content: str) -> Dict[str, Any]:
        """
        Analyze the complexity of content to determine appropriate personalization level
        """
        try:
            # Simple complexity analysis based on content characteristics
            word_count = len(content.split())
            sentence_count = len([s for s in content.split('.') if s.strip()])
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

            # Count technical terms (simple heuristic)
            technical_terms = [
                'algorithm', 'protocol', 'framework', 'architecture', 'component',
                'system', 'interface', 'function', 'method', 'class', 'object',
                'variable', 'parameter', 'configuration', 'optimization'
            ]

            technical_term_count = sum(1 for term in technical_terms if term.lower() in content.lower())

            complexity_score = (
                (avg_sentence_length * 0.1) +
                (technical_term_count * 0.5) +
                (word_count / 100 * 0.1)
            )

            # Determine complexity level
            if complexity_score < 5:
                complexity_level = "low"
            elif complexity_score < 10:
                complexity_level = "medium"
            else:
                complexity_level = "high"

            return {
                "complexity_score": complexity_score,
                "complexity_level": complexity_level,
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": avg_sentence_length,
                "technical_terms_count": technical_term_count
            }

        except Exception as e:
            logger.error(f"Error analyzing content complexity: {e}")
            return {
                "complexity_score": 0,
                "complexity_level": "unknown",
                "word_count": 0,
                "sentence_count": 0,
                "avg_sentence_length": 0,
                "technical_terms_count": 0
            }

    @staticmethod
    async def identify_content_type(content: str) -> str:
        """
        Identify the type of content for appropriate personalization
        """
        try:
            content_lower = content.lower()

            # Content type identification based on keywords
            if any(keyword in content_lower for keyword in ['code', 'function', 'algorithm', 'programming', 'implementation']):
                return "technical_code"
            elif any(keyword in content_lower for keyword in ['theory', 'concept', 'principle', 'definition', 'model']):
                return "theoretical"
            elif any(keyword in content_lower for keyword in ['example', 'case', 'scenario', 'application', 'use']):
                return "practical_example"
            elif any(keyword in content_lower for keyword in ['equation', 'formula', 'math', 'calculation']):
                return "mathematical"
            elif any(keyword in content_lower for keyword in ['diagram', 'figure', 'image', 'visual']):
                return "visual_description"
            else:
                return "general"

        except Exception as e:
            logger.error(f"Error identifying content type: {e}")
            return "general"

    @staticmethod
    async def extract_key_concepts(content: str) -> List[str]:
        """
        Extract key concepts from content for targeted personalization
        """
        try:
            # Simple keyword extraction based on common technical terms
            key_concepts = []

            # Common concepts in AI and robotics
            concept_patterns = [
                'neural network', 'machine learning', 'deep learning', 'robotics', 'ai',
                'algorithm', 'sensor', 'actuator', 'control system', 'feedback',
                'computer vision', 'path planning', 'kinematics', 'dynamics',
                'locomotion', 'manipulation', 'autonomy', 'navigation'
            ]

            content_lower = content.lower()
            for pattern in concept_patterns:
                if pattern in content_lower and pattern not in key_concepts:
                    key_concepts.append(pattern)

            # Extract capitalized terms (potential proper nouns)
            words = content.split()
            for word in words:
                clean_word = word.strip('.,;:!?()[]{}"\'')
                if clean_word and clean_word[0].isupper() and len(clean_word) > 3 and clean_word not in key_concepts:
                    key_concepts.append(clean_word)

            return key_concepts

        except Exception as e:
            logger.error(f"Error extracting key concepts: {e}")
            return []

    @staticmethod
    async def adapt_for_background(content: str, user_background: str, content_type: str = "general") -> str:
        """
        Adapt content based on user background and content type
        """
        try:
            adapted_content = content

            if user_background == "software-focused":
                if content_type == "theoretical":
                    adapted_content += "\n\n*Software Implementation Note: This concept can be implemented using [relevant programming approach/algorithm].*"
                elif content_type == "practical_example":
                    adapted_content += "\n\n*Implementation Tip: Consider using [relevant software framework/library] for this approach.*"

            elif user_background == "hardware-focused":
                if content_type == "theoretical":
                    adapted_content += "\n\n*Hardware Implementation Note: This concept can be realized using [relevant hardware components/systems].*"
                elif content_type == "practical_example":
                    adapted_content += "\n\n*Hardware Tip: Ensure [relevant hardware considerations] when implementing this approach.*"

            elif user_background == "mixed":
                if content_type == "theoretical":
                    adapted_content += "\n\n*Implementation Note: This concept involves both software algorithms and hardware components for complete realization.*"
                elif content_type == "practical_example":
                    adapted_content += "\n\n*Integration Tip: Consider both software and hardware aspects when implementing this approach.*"

            elif user_background == "beginner":
                adapted_content += "\n\n*Beginner Tip: Focus on understanding the core concepts before diving into implementation details.*"

            return adapted_content

        except Exception as e:
            logger.error(f"Error adapting content for background: {e}")
            return content

# Singleton instance
personalization_skills = PersonalizationSkills()