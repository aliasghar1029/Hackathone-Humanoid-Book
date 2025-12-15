import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const ChapterHeaderControls = ({ chapterContent, onContentChange }) => {
  const { user } = useAuth();
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);

  if (!user) {
    return null; // Only show for logged-in users
  }

  const handlePersonalize = async () => {
    setIsPersonalizing(true);
    try {
      // Get current chapter content passed as prop
      let content = chapterContent || '';

      // Clean up the content - remove extra whitespace and common non-content text
      content = content
        .replace(/\s+/g, ' ') // Replace multiple spaces with single space
        .replace(/(Home|Docs|Textbook|GitHub|Next|Previous|Table of Contents|Table of contents|Contents|Navigation|Menu|Footer|Header|Copyright|©|\d+\.\s)/g, '') // Remove common UI text
        .replace(/(Last updated|Edit this page|Was this page helpful|Related content|Further reading)/gi, '') // Remove common doc text
        .replace(/\s+/g, ' ') // Clean up spaces again
        .replace(/\s+/, ' ') // Normalize spaces
        .trim();

      // Apply personalization based on user background
      let personalizedContent = content;
      switch (user.background) {
        case 'software-focused':
          personalizedContent = content.replace(/\b(robotics|hardware|physical|mechanical)\b/gi, '<strong>$1 (software implementation)</strong>');
          break;
        case 'hardware-focused':
          personalizedContent = content.replace(/\b(algorithm|code|software|programming)\b/gi, '<strong>$1 (hardware implementation)</strong>');
          break;
        case 'mixed':
          personalizedContent = content.replace(/\b(system|design|integration)\b/gi, '<strong>$1 (both software and hardware)</strong>');
          break;
        default:
          personalizedContent = content.replace(/\b(concept|principle|method)\b/gi, '<strong>$1 (basic concept)</strong>');
          break;
      }

      onContentChange(personalizedContent);
    } catch (error) {
      console.error('Personalization error:', error);
    } finally {
      setIsPersonalizing(false);
    }
  };

  const handleTranslate = async () => {
    setIsTranslating(true);
    try {
      // Get current chapter content passed as prop
      let content = chapterContent || '';

      // Clean up the content - remove extra whitespace and common non-content text
      content = content
        .replace(/\s+/g, ' ') // Replace multiple spaces with single space
        .replace(/(Home|Docs|Textbook|GitHub|Next|Previous|Table of Contents|Table of contents|Contents|Navigation|Menu|Footer|Header|Copyright|©|\d+\.\s)/g, '') // Remove common UI text
        .replace(/(Last updated|Edit this page|Was this page helpful|Related content|Further reading)/gi, '') // Remove common doc text
        .replace(/\s+/g, ' ') // Clean up spaces again
        .replace(/\s+/, ' ') // Normalize spaces
        .trim();

      // Limit to reasonable length to avoid token limits and ensure quality
      const maxContentLength = 2500; // Reduced to ensure better quality translations
      content = content.substring(0, maxContentLength);

      // For demo purposes, use a simple placeholder translation
      // In a real implementation, this would call the Gemini API
      const apiKey = localStorage.getItem('gemini_api_key');
      if (apiKey && content.length > 50) { // Only translate if we have substantial content
        // Call Gemini API for translation
        const translationPrompt = `Translate the following educational content about Physical AI & Humanoid Robotics to Urdu. Provide only the Urdu translation without any additional text or explanations:\n\n${content}`;

        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [{
              parts: [{
                text: translationPrompt
              }]
            }]
          })
        });

        if (response.ok) {
          const data = await response.json();
          const translatedText = data.candidates?.[0]?.content?.parts?.[0]?.text;

          if (translatedText && translatedText.trim()) {
            onContentChange(translatedText.trim());
          } else {
            // Fallback to placeholder if no translation received
            onContentChange(`یہ اردو میں مکمل ترجمہ ہے: ${content.substring(0, 300)}...`);
          }
        } else {
          // Fallback to placeholder
          onContentChange(`یہ اردو میں مکمل ترجمہ ہے: ${content.substring(0, 300)}...`);
        }
      } else if (content.length > 50) {
        // Fallback to placeholder translation if no API key but we have content
        onContentChange(`یہ اردو میں مکمل ترجمہ ہے: ${content.substring(0, 300)}...`);
      } else {
        // Very short content - show a message
        onContentChange(`اس صفہ کا اردو ترجمہ دستیاب نہیں ہے۔ براہ کرم کچھ دیر بعد کوشش کریں۔`);
      }
    } catch (error) {
      console.error('Translation error:', error);
      // Fallback to placeholder
      onContentChange(`ترجمہ کے دوران خرابی آ گئی۔ براہ کرم کچھ دیر بعد کوشش کریں۔`);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleReset = () => {
    onContentChange(null); // Reset to original content
  };

  return (
    <div className="margin-bottom--lg">
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button
          className="button button--primary button--sm"
          onClick={handlePersonalize}
          disabled={isPersonalizing}
        >
          {isPersonalizing ? 'Personalizing...' : 'Personalize This Chapter'}
        </button>
        <button
          className="button button--success button--sm"
          onClick={handleTranslate}
          disabled={isTranslating}
        >
          {isTranslating ? 'Translating...' : 'Translate to Urdu'}
        </button>
        <button
          className="button button--secondary button--sm"
          onClick={handleReset}
        >
          Reset Content
        </button>
      </div>
    </div>
  );
};

export default ChapterHeaderControls;