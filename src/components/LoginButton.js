import React from 'react';
import { useUser } from '../contexts/UserContext';
import './LoginButton.css';

const LoginButton = ({ onOpenAuthModal }) => {
  const { user, logout } = useUser();

  if (user) {
    return (
      <div className="user-menu">
        <span className="user-name">Hi, {user.name}!</span>
        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </div>
    );
  }

  return (
    <button className="login-btn" onClick={onOpenAuthModal}>
      Login / Sign Up
    </button>
  );
};

export default LoginButton;