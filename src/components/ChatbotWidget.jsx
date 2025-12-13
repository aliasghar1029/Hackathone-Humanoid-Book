import React, { useState, useEffect, useRef } from 'react';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Function to get selected text from the page
  const getSelectedText = () => {
    const selectedText = window.getSelection().toString().trim();
    return selectedText;
  };

  // Handle text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const text = getSelectedText();
      if (text && text.length > 10) { // Only consider meaningful selections
        setSelectedText(text);
        if (isOpen && inputRef.current) {
          // Auto-fill input when chat is open and text is selected
          setInputValue(`Explain this: ${text}`);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [isOpen]);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // When opening, check for selected text and auto-fill if available
      const text = getSelectedText();
      if (text && text.length > 10 && !inputValue) {
        setInputValue(`Explain this: ${text}`);
      }
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    const textToSend = selectedText || null;
    setInputValue('');
    setIsLoading(true);

    try {
      // Sanitize the text before sending
      const sanitizedQuery = inputValue.replace(/[\r\n\t]/g, ' ').trim();
      const sanitizedSelectedText = selectedText ? selectedText.replace(/[\r\n\t]/g, ' ').trim() : null;

      // Set a longer timeout for the fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout

      const response = await fetch('/query', {  // Using proxy path
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: sanitizedQuery,
          selected_text: sanitizedSelectedText,
        }),
        signal: controller.signal  // Add abort signal for timeout
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // The backend now returns 'answer' instead of 'response'
      const botMessage = {
        id: Date.now() + 1,
        text: data.answer || data.response || "I couldn't generate a response. Please try again.",
        sender: 'bot',
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMessageText = 'Sorry, I encountered an error connecting to the backend. ';

      if (error.name === 'AbortError') {
        errorMessageText += 'The request timed out. The backend may be processing your request for too long. Please try a simpler question or wait a moment before trying again.';
      } else if (error instanceof TypeError && error.message.includes('fetch')) {
        errorMessageText += 'The backend server may not be running. Please ensure:\n1. Backend is running at http://127.0.0.1:8000\n2. Proxy is configured correctly in docusaurus.config.js';
      } else if (error.message.includes('404')) {
        errorMessageText += 'The API endpoint may not be available. Check if the backend server is running.';
      } else if (error.message.includes('504')) {
        errorMessageText += 'The gateway timed out. The backend server may be overloaded or taking too long to respond. Please try again in a moment.';
      } else if (error.message.includes('500')) {
        errorMessageText += 'The backend server encountered an error. Check the backend logs for details.';
      } else if (error.message.includes('NetworkError')) {
        errorMessageText += 'Network connection failed. Ensure the backend is running and accessible.';
      } else {
        errorMessageText += `Details: ${error.message}`;
      }

      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'bot',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSelectedText('');
    setInputValue('');
  };

  return (
    <div className="chatbot-widget">
      {isOpen ? (
        <div className="chatbot-modal">
          <div className="chatbot-header">
            <div className="chatbot-title">🤖 Humanoid AI</div>
            <div className="chatbot-controls">
              <button onClick={clearChat} className="clear-btn" title="Clear chat">
                <ClearIcon />
              </button>
              <button onClick={toggleChat} className="close-btn" title="Close">
                <CloseIcon />
              </button>
            </div>
          </div>
          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <h3>Hello! I'm your Humanoid Robotics Assistant</h3>
                <p>Ask me anything about the Physical AI & Humanoid Robotics textbook.</p>
                <p>Select text on the page to include it in your query.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  <div className="message-content">
                    {message.sender === 'bot' && (
                      <div className="bot-icon">
                        <BotIcon />
                      </div>
                    )}
                    <div className="message-text">
                      {message.text.split('\n').map((line, i) => (
                        <React.Fragment key={i}>
                          {line}
                          <br />
                        </React.Fragment>
                      ))}
                    </div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content">
                  <div className="bot-icon">
                    <BotIcon />
                  </div>
                  <div className="message-text loading">
                    <span className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          {selectedText && (
            <div className="selected-text-preview">
              <span className="selected-label">Selected:</span> {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}
              <button onClick={() => {
                setSelectedText('');
                if (inputValue.startsWith('Explain this:')) {
                  setInputValue('');
                }
              }} className="remove-selection">
                ×
              </button>
            </div>
          )}
          <div className="chatbot-input-area">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about humanoid robotics..."
              className="chatbot-input"
              rows="1"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              {isLoading ? <LoadingSpinner /> : <SendIcon />}
            </button>
          </div>
        </div>
      ) : (
        <button className="chatbot-button" onClick={toggleChat}>
          <RobotIcon />
        </button>
      )}
    </div>
  );
};

// SVG Icons
const RobotIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 19V21C6 21.5523 6.44772 22 7 22H17C17.5523 22 18 21.5523 18 21V19" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <path d="M10 5L8 7L10 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M14 5L16 7L14 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M8 12H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 16V12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <path d="M9 2V5" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <path d="M15 2V5" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <rect x="4" y="5" width="16" height="12" rx="2" stroke="currentColor" strokeWidth="2"/>
  </svg>
);

const SendIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ClearIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M19 7L18.1327 19.1425C18.0579 20.1891 17.1882 21 16.1378 21H7.86224C6.81184 21 5.94208 20.1891 5.86732 19.1425L5 7M10 11V17M14 11V17M15 7V4C15 3.44772 14.5523 3 14 3H10C9.44772 3 9 3.44772 9 4V7M4 7H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const BotIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 11L11 13L9 15M15 11L13 13L15 15M18 12C18 8.68629 15.3137 6 12 6C8.68629 6 6 8.68629 6 12C6 15.3137 8.68629 18 12 18C15.3137 18 18 15.3137 18 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M13 11H13.01M11 15H11.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const LoadingSpinner = () => (
  <svg className="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M19.0784 4.99994L16.25 7.82837M4.92157 19.0784L7.75 16.25M4.92157 4.99994L7.75 7.82837" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export default ChatbotWidget;