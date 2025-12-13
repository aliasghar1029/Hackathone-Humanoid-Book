import React, { useState } from 'react';
import { useUser } from '../contexts/UserContext';
import './PersonalizeButton.css';

const PersonalizeButton = ({ content, title }) => {
  const { user } = useUser();
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [personalizedContent, setPersonalizedContent] = useState(null);
  const [showOriginal, setShowOriginal] = useState(true);

  const handlePersonalize = async () => {
    if (!user) {
      alert('Please log in to use personalization features');
      return;
    }

    setIsPersonalizing(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify({
          content,
          user_profile: {
            hardware: user.hardware,
            experience: user.experience,
            language: user.language
          },
          title
        })
      });

      if (response.ok) {
        const result = await response.json();
        setPersonalizedContent(result.personalized_content);
        setShowOriginal(false);
      } else {
        alert('Failed to personalize content');
      }
    } catch (error) {
      console.error('Error personalizing content:', error);
      alert('Error personalizing content');
    } finally {
      setIsPersonalizing(false);
    }
  };

  const handleReset = () => {
    setPersonalizedContent(null);
    setShowOriginal(true);
  };

  return (
    <div className="personalize-section">
      <div className="personalize-controls">
        <button
          className="personalize-btn"
          onClick={handlePersonalize}
          disabled={isPersonalizing || !user}
        >
          {isPersonalizing ? 'Personalizing...' : 'Personalize for me'}
        </button>

        {!showOriginal && (
          <button
            className="reset-btn"
            onClick={handleReset}
          >
            Show Original
          </button>
        )}

        {!showOriginal && (
          <button
            className="toggle-view-btn"
            onClick={() => setShowOriginal(!showOriginal)}
          >
            {showOriginal ? 'Show Personalized' : 'Show Original'}
          </button>
        )}
      </div>

      {personalizedContent && !showOriginal ? (
        <div className="personalized-content">
          <h3>Personalized for you (Hardware: {user?.hardware}, Experience: {user?.experience})</h3>
          <div dangerouslySetInnerHTML={{ __html: personalizedContent }} />
        </div>
      ) : (
        <div className="original-content" style={{ display: showOriginal ? 'block' : 'none' }}>
          {typeof content === 'string' ? <div dangerouslySetInnerHTML={{ __html: content }} /> : content}
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;