import React, { useState, useEffect } from 'react';
import OriginalLayout from '@theme-original/DocItem/Layout';
import { useAuth } from '../../../contexts/AuthContext';
import ChapterHeaderControls from '../../../components/ChapterHeaderControls';

export default function Layout(props) {
  const { user } = useAuth();
  const [modifiedContent, setModifiedContent] = useState(null);
  const [originalContent, setOriginalContent] = useState(null);

  // Get the original content from the page
  useEffect(() => {
    if (props.content) {
      // Extract content from the MDX component
      const content = props.content;
      if (content.meta) {
        setOriginalContent(content.meta.unifiedNav);
      }
    }
  }, [props.content]);

  const handleContentChange = (newContent) => {
    setModifiedContent(newContent);
  };

  // For now, just render the controls above the original content
  // In a full implementation, we'd replace the content with modifiedContent when available
  return (
    <>
      {user && (
        <ChapterHeaderControls
          chapterContent={originalContent || ''}
          onContentChange={handleContentChange}
        />
      )}
      <OriginalLayout {...props} />
    </>
  );
}