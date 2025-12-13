import React, { useState } from 'react';
import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import './AuthModal.css';

const AuthModal = ({ isOpen, onClose }) => {
  const [isLoginView, setIsLoginView] = useState(true);

  if (!isOpen) return null;

  return (
    <div className="auth-modal-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
        <div className="auth-modal-header">
          <h2>{isLoginView ? 'Welcome Back' : 'Create Account'}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <div className="auth-modal-content">
          {isLoginView ? (
            <LoginForm
              onSwitchToSignup={() => setIsLoginView(false)}
            />
          ) : (
            <SignupForm
              onSwitchToLogin={() => setIsLoginView(true)}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthModal;