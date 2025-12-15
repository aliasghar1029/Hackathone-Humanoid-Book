"""
Claude Subagent for personalization logic
"""
import asyncio
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class PersonalizationAgent:
    """
    Claude Subagent for handling content personalization based on user background
    """

    def __init__(self):
        self.personalization_rules = {
            "software-focused": {
                "technical_depth": "high",
                "examples": ["code snippets", "algorithm analysis", "implementation details"],
                "terminology": "technical",
                "focus": "software architecture and implementation"
            },
            "hardware-focused": {
                "technical_depth": "high",
                "examples": ["circuit diagrams", "physical components", "mechanical systems"],
                "terminology": "hardware-oriented",
                "focus": "physical implementation and hardware systems"
            },
            "mixed": {
                "technical_depth": "balanced",
                "examples": ["both software and hardware", "integration examples", "system design"],
                "terminology": "balanced",
                "focus": "system integration and full-stack concepts"
            },
            "beginner": {
                "technical_depth": "low",
                "examples": ["simplified explanations", "basic concepts", "step-by-step guides"],
                "terminology": "simplified",
                "focus": "fundamental concepts and basic understanding"
            }
        }

    async def personalize_content(self, content: str, user_background: str, preferences: Dict[str, Any] = None) -> str:
        """
        Apply personalization rules to content based on user background
        """
        try:
            if not user_background or user_background not in self.personalization_rules:
                return content  # Return original content if no valid background

            rules = self.personalization_rules[user_background]

            # Apply personalization transformations based on rules
            personalized_content = content

            # Adjust technical depth
            if rules["technical_depth"] == "low":
                # Simplify content for beginners
                personalized_content = self._simplify_content(personalized_content)
            elif rules["technical_depth"] == "high":
                # Add technical details for advanced users
                personalized_content = self._add_technical_details(personalized_content, user_background)

            # Add relevant examples based on background
            personalized_content = self._add_relevant_examples(personalized_content, rules["examples"])

            # Adjust terminology based on background
            personalized_content = self._adjust_terminology(personalized_content, rules["terminology"])

            logger.info(f"Content personalized for {user_background} background")
            return personalized_content

        except Exception as e:
            logger.error(f"Error in personalization: {e}")
            return content  # Return original content on error

    def _simplify_content(self, content: str) -> str:
        """
        Simplify content for beginner users
        """
        # Remove complex technical jargon and replace with simpler explanations
        simplified = content.replace("algorithmic complexity", "how efficient the method is")
        simplified = simplified.replace("asynchronous processing", "doing multiple things at once")
        simplified = simplified.replace("optimization", "making it work better")
        return simplified

    def _add_technical_details(self, content: str, background: str) -> str:
        """
        Add technical details for advanced users
        """
        detailed = content
        if background == "software-focused":
            detailed = detailed.replace(
                "system",
                "system (with considerations for software architecture, data flow, and implementation patterns)"
            )
        elif background == "hardware-focused":
            detailed = detailed.replace(
                "component",
                "component (with attention to physical properties, electrical characteristics, and mechanical constraints)"
            )
        return detailed

    def _add_relevant_examples(self, content: str, examples: List[str]) -> str:
        """
        Add relevant examples based on user background
        """
        # In a real implementation, this would add specific examples
        # For now, we'll add placeholder indicators
        example_text = f"\n\n**Relevant Examples for You:** {', '.join(examples)}"
        return content + example_text

    def _adjust_terminology(self, content: str, terminology: str) -> str:
        """
        Adjust terminology based on user background
        """
        if terminology == "simplified":
            # Use simpler terms
            adjusted = content.replace("implementation", "way of doing it")
            adjusted = adjusted.replace("architecture", "design")
            return adjusted
        elif terminology == "hardware-oriented":
            # Emphasize hardware aspects
            adjusted = content.replace("system", "hardware system")
            adjusted = adjusted.replace("component", "hardware component")
            return adjusted
        elif terminology == "technical":
            # Keep technical terms
            return content
        else:
            # Balanced terminology
            return content

# Singleton instance
personalization_agent = PersonalizationAgent()