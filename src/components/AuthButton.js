import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './AuthButton.css';

const AuthButton = () => {
  const { user, login, logout, signup } = useAuth();
  const [showModal, setShowModal] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    hardware: '',
    experience: '',
    language: 'English'
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (isLogin) {
      const result = await login(formData.email, formData.password);
      if (result.success) {
        setShowModal(false);
      } else {
        alert(result.error);
      }
    } else {
      const result = await signup(formData);
      if (result.success) {
        setShowModal(false);
      } else {
        alert(result.error);
      }
    }

    setLoading(false);
  };

  const handleLogout = () => {
    logout();
  };

  if (user) {
    return (
      <div className="auth-button-container">
        <span className="user-greeting">Hi, {user.name}!</span>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className="auth-button-container">
      <button className="auth-button" onClick={() => setShowModal(true)}>
        Login / Sign Up
      </button>

      {showModal && (
        <div className="auth-modal-overlay">
          <div className="auth-modal">
            <div className="auth-modal-header">
              <h3>{isLogin ? 'Login' : 'Sign Up'}</h3>
              <button className="close-button" onClick={() => setShowModal(false)}>
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              {!isLogin && (
                <div className="form-group">
                  <label>Name:</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    required={!isLogin}
                    disabled={isLogin}
                  />
                </div>
              )}

              <div className="form-group">
                <label>Email:</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Password:</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  required
                />
              </div>

              {!isLogin && (
                <>
                  <div className="form-group">
                    <label>Hardware:</label>
                    <select
                      value={formData.hardware}
                      onChange={(e) => setFormData({...formData, hardware: e.target.value})}
                      required
                    >
                      <option value="">Select Hardware</option>
                      <option value="Jetson">Jetson</option>
                      <option value="Laptop">Laptop</option>
                      <option value="Raspberry Pi">Raspberry Pi</option>
                      <option value="Arduino">Arduino</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Experience Level:</label>
                    <select
                      value={formData.experience}
                      onChange={(e) => setFormData({...formData, experience: e.target.value})}
                      required
                    >
                      <option value="">Select Level</option>
                      <option value="Beginner">Beginner</option>
                      <option value="Intermediate">Intermediate</option>
                      <option value="Advanced">Advanced</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Language:</label>
                    <select
                      value={formData.language}
                      onChange={(e) => setFormData({...formData, language: e.target.value})}
                      required
                    >
                      <option value="English">English</option>
                      <option value="Urdu">Urdu</option>
                    </select>
                  </div>
                </>
              )}

              <button type="submit" disabled={loading} className="submit-button">
                {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
              </button>
            </form>

            <div className="auth-switch">
              <button onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? 'Need an account? Sign Up' : 'Already have an account? Login'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuthButton;