import React, { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import ChapterToolbar from '../components/ChapterToolbar';

const DocItemWrapper = ({ children, content }) => {
  const { user } = useAuth();
  const [currentContent, setCurrentContent] = useState(content);

  // Reset content when user changes or component mounts
  useEffect(() => {
    setCurrentContent(content);
  }, [content]);

  // Only show toolbar on doc pages when user is authenticated
  const isDocPage = typeof window !== 'undefined' &&
    window.location.pathname.includes('/docs/');

  if (!isDocPage || !user) {
    return <>{children}</>;
  }

  return (
    <div style={{ position: 'relative' }}>
      <ChapterToolbar
        content={currentContent || ''}
        onContentChange={setCurrentContent}
        user={user}
      />
      <div>
        {currentContent ? (
          <div dangerouslySetInnerHTML={{ __html: currentContent }} />
        ) : (
          children
        )}
      </div>
    </div>
  );
};

export default DocItemWrapper;