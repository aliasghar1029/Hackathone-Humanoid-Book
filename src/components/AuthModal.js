import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const AuthModal = ({ isOpen, onClose }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    background: '',
    hardware: '',
    experience: '',
    language: 'English'
  });
  const [error, setError] = useState('');
  const { login, signup } = useAuth();

  if (!isOpen) return null;

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isLogin) {
      // Login
      const result = login(formData.email, formData.password);
      if (result.success) {
        onClose();
      } else {
        setError(result.error);
      }
    } else {
      // Signup - validate required fields
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match');
        return;
      }

      if (!formData.background) {
        setError('Please select your background');
        return;
      }

      const signupData = {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        background: formData.background,
        hardware: formData.hardware,
        experience: formData.experience,
        language: formData.language
      };

      const result = await signup(signupData);
      if (result.success) {
        onClose();
      } else {
        setError(result.error);
      }
    }
  };

  return (
    <div className="modal" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000
    }} onClick={onClose}>
      <div className="modal-dialog" style={{
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '0.5rem',
        maxWidth: '500px',
        width: '90%',
        margin: '1rem'
      }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{isLogin ? 'Login' : 'Sign Up'}</h3>
          <button
            className="close-button"
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer'
            }}
          >
            &times;
          </button>
        </div>

        <div className="modal-body">
          {error && (
            <div className="alert alert--danger margin-bottom--md">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <div className="margin-bottom--md">
                <label htmlFor="name" className="form-label">Full Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required={!isLogin}
                  className="form-control"
                />
              </div>
            )}

            <div className="margin-bottom--md">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>

            <div className="margin-bottom--md">
              <label htmlFor="password" className="form-label">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>

            {!isLogin && (
              <div className="margin-bottom--md">
                <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required={!isLogin}
                  className="form-control"
                />
              </div>
            )}

            {!isLogin && (
              <>
                <div className="margin-bottom--md">
                  <label htmlFor="background" className="form-label">Background</label>
                  <select
                    id="background"
                    name="background"
                    value={formData.background}
                    onChange={handleChange}
                    required={!isLogin}
                    className="form-control"
                  >
                    <option value="">Select your background</option>
                    <option value="software-focused">Software-focused</option>
                    <option value="hardware-focused">Hardware-focused</option>
                    <option value="mixed">Mixed background</option>
                    <option value="beginner">Beginner</option>
                  </select>
                </div>

                <div className="margin-bottom--md">
                  <label htmlFor="hardware" className="form-label">Current Hardware</label>
                  <select
                    id="hardware"
                    name="hardware"
                    value={formData.hardware}
                    onChange={handleChange}
                    className="form-control"
                  >
                    <option value="">Select your hardware</option>
                    <option value="Jetson">Jetson</option>
                    <option value="Laptop">Laptop/Desktop</option>
                    <option value="Raspberry Pi">Raspberry Pi</option>
                    <option value="Arduino">Arduino</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="margin-bottom--md">
                  <label htmlFor="experience" className="form-label">Experience Level</label>
                  <select
                    id="experience"
                    name="experience"
                    value={formData.experience}
                    onChange={handleChange}
                    className="form-control"
                  >
                    <option value="">Select your experience</option>
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>

                <div className="margin-bottom--md">
                  <label htmlFor="language" className="form-label">Preferred Language</label>
                  <select
                    id="language"
                    name="language"
                    value={formData.language}
                    onChange={handleChange}
                    className="form-control"
                  >
                    <option value="English">English</option>
                    <option value="Urdu">Urdu</option>
                  </select>
                </div>
              </>
            )}

            <div className="button-group--responsive" style={{ display: 'flex', gap: '0.5rem' }}>
              <button type="submit" className="button button--primary button--block">
                {isLogin ? 'Login' : 'Sign Up'}
              </button>
            </div>
          </form>
        </div>

        <div className="modal-footer">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              className="button button--link"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? 'Sign up' : 'Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;