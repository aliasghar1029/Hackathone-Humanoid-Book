import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './ChapterToolbar.css';

const ChapterToolbar = () => {
  const { user } = useAuth();
  const [showButtons, setShowButtons] = useState(false);
  const [content, setContent] = useState('');

  // Get the current page content to personalize/translate
  useEffect(() => {
    const mainContent = document.querySelector('main .container');
    if (mainContent) {
      setContent(mainContent.innerText || '');
    }
  }, []);

  const handlePersonalize = async () => {
    if (!user) {
      alert('Please log in to use this feature');
      return;
    }

    try {
      const response = await fetch('/api/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify({
          content: content.substring(0, 1000), // Limit content size
          user_profile: {
            hardware: user.hardware,
            experience: user.experience,
            language: user.language
          },
          title: document.title
        })
      });

      if (response.ok) {
        const result = await response.json();
        // For now, just show an alert with the result
        alert('Content personalized! (Check console for details)');
        console.log('Personalized content:', result.personalized_content);
      } else {
        alert('Failed to personalize content');
      }
    } catch (error) {
      console.error('Error personalizing content:', error);
      alert('Error personalizing content');
    }
  };

  const handleTranslate = async () => {
    if (!user) {
      alert('Please log in to use this feature');
      return;
    }

    try {
      const response = await fetch('/api/translate_urdu', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify({
          content: content.substring(0, 1000), // Limit content size
          title: document.title
        })
      });

      if (response.ok) {
        const result = await response.json();
        // For now, just show an alert with the result
        alert('Content translated to Urdu! (Check console for details)');
        console.log('Urdu content:', result.urdu_content);
      } else {
        alert('Failed to translate content');
      }
    } catch (error) {
      console.error('Error translating content:', error);
      alert('Error translating content');
    }
  };

  if (!user) {
    return null; // Only show buttons if user is logged in
  }

  return (
    <div className="chapter-toolbar">
      <button className="toolbar-btn personalize-btn" onClick={handlePersonalize} title="Personalize for me">
        🎯 Personalize
      </button>
      <button className="toolbar-btn urdu-btn" onClick={handleTranslate} title="اردو میں پڑھیں">
        🇵🇰 اردو میں
      </button>
    </div>
  );
};

export default ChapterToolbar;