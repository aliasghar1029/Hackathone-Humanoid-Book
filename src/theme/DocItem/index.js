import React, { useState } from 'react';
import OriginalDocItem from '@theme-original/DocItem';
import { useAuth } from '@site/src/contexts/AuthContext';
import ChapterControls from '@site/src/components/ChapterControls';
import AuthModal from '@site/src/components/AuthModal';

// This is a swizzled DocItem component that adds chapter controls
export default function DocItem(props) {
  const { user } = useAuth();
  const [contentState, setContentState] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);

  const handleContentChange = (newContent) => {
    setContentState(newContent);
  };

  const handleAuthAction = (mode) => {
    setShowAuthModal(true);
  };

  return (
    <>
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col">
            {/* Show controls for logged-in users or auth buttons for guests */}
            {!user ? (
              <div className="margin-bottom--lg text--center">
                <p>Please login to access personalization features</p>
                <button
                  className="button button--primary margin-right--sm"
                  onClick={() => handleAuthAction('login')}
                >
                  Login
                </button>
                <button
                  className="button button--secondary"
                  onClick={() => handleAuthAction('signup')}
                >
                  Sign Up
                </button>
              </div>
            ) : (
              <ChapterControls onContentChange={handleContentChange} />
            )}

            {/* Render content - either modified or original */}
            {contentState ? (
              <article className="markdown">
                <div
                  className="post-content"
                  dangerouslySetInnerHTML={{ __html: contentState }}
                />
              </article>
            ) : (
              <OriginalDocItem {...props} />
            )}
          </div>
        </div>
      </div>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
      />
    </>
  );
}