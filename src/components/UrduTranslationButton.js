import React, { useState } from 'react';
import { useUser } from '../contexts/UserContext';
import './UrduTranslationButton.css';

const UrduTranslationButton = ({ content, title }) => {
  const { user } = useUser();
  const [isTranslating, setIsTranslating] = useState(false);
  const [urduContent, setUrduContent] = useState(null);
  const [showUrdu, setShowUrdu] = useState(false);

  const handleTranslate = async () => {
    if (!user) {
      alert('Please log in to use translation features');
      return;
    }

    setIsTranslating(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/translate_urdu', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify({
          content,
          title
        })
      });

      if (response.ok) {
        const result = await response.json();
        setUrduContent(result.urdu_content);
        setShowUrdu(true);
      } else {
        alert('Failed to translate content');
      }
    } catch (error) {
      console.error('Error translating content:', error);
      alert('Error translating content');
    } finally {
      setIsTranslating(false);
    }
  };

  const handleReset = () => {
    setUrduContent(null);
    setShowUrdu(false);
  };

  return (
    <div className="urdu-translation-section">
      <div className="urdu-translation-controls">
        <button
          className="urdu-translate-btn"
          onClick={handleTranslate}
          disabled={isTranslating || !user}
        >
          {isTranslating ? 'Translating...' : 'اردو میں پڑھیں'}
        </button>

        {urduContent && (
          <button
            className="urdu-reset-btn"
            onClick={handleReset}
          >
            Original
          </button>
        )}

        {urduContent && (
          <button
            className="urdu-toggle-btn"
            onClick={() => setShowUrdu(!showUrdu)}
          >
            {showUrdu ? 'Show Original' : 'Show Urdu'}
          </button>
        )}
      </div>

      {urduContent && showUrdu && (
        <div className="urdu-content">
          <h3>اردو ترجمہ</h3>
          <div dangerouslySetInnerHTML={{ __html: urduContent }} dir="rtl" />
        </div>
      )}

      {urduContent && !showUrdu && (
        <div className="original-content-urdu">
          {typeof content === 'string' ? <div dangerouslySetInnerHTML={{ __html: content }} /> : content}
        </div>
      )}
    </div>
  );
};

export default UrduTranslationButton;