import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';

const SignupForm = ({ onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    hardware: '',
    experience: '',
    language: 'English',
    background: '' // Add background field for personalization
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { signup } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!formData.background) {
      setError('Please select your background');
      return;
    }

    setLoading(true);
    setError('');

    // Prepare signup data
    const signupData = {
      name: formData.name,
      email: formData.email,
      password: formData.password, // This will be removed in AuthContext for security
      background: formData.background,
      hardware: formData.hardware,
      experience: formData.experience,
      language: formData.language
    };

    const result = await signup(signupData);
    setLoading(false);

    if (!result.success) {
      setError(result.error);
    }
  };

  return (
    <div className="container margin-vert--lg">
      <div className="row">
        <div className="col col--6 col--offset-3">
          <div className="card">
            <div className="card__header">
              <h2>Create Account</h2>
            </div>
            <div className="card__body">
              {error && <div className="alert alert--danger margin-bottom--md">{error}</div>}

              <form onSubmit={handleSubmit}>
                <div className="margin-bottom--md">
                  <label htmlFor="name" className="form-label">Full Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="form-control"
                  />
                </div>

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

                <div className="margin-bottom--md">
                  <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    className="form-control"
                  />
                </div>

                <div className="margin-bottom--md">
                  <label htmlFor="background" className="form-label">Background</label>
                  <select
                    id="background"
                    name="background"
                    value={formData.background}
                    onChange={handleChange}
                    required
                    className="form-control"
                  >
                    <option value="">Select your background</option>
                    <option value="software-focused">Software-focused (programming, AI, algorithms)</option>
                    <option value="hardware-focused">Hardware-focused (electronics, robotics, mechanics)</option>
                    <option value="mixed">Mixed background (both software and hardware)</option>
                    <option value="beginner">Beginner (learning both software and hardware)</option>
                  </select>
                  <div className="form-text">This will help us personalize your learning experience</div>
                </div>

                <div className="margin-bottom--md">
                  <label htmlFor="hardware" className="form-label">Current Hardware</label>
                  <select
                    id="hardware"
                    name="hardware"
                    value={formData.hardware}
                    onChange={handleChange}
                    required
                    className="form-control"
                  >
                    <option value="">Select your hardware</option>
                    <option value="Jetson">Jetson (Nano, Xavier, etc.)</option>
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
                    required
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
                    required
                    className="form-control"
                  >
                    <option value="English">English</option>
                    <option value="Urdu">Urdu</option>
                  </select>
                </div>

                <button type="submit" disabled={loading} className={`button button--primary button--block ${loading ? 'button--disabled' : ''}`}>
                  {loading ? 'Creating Account...' : 'Sign Up'}
                </button>
              </form>

              <div className="margin-top--md">
                <p>
                  Already have an account?{' '}
                  <button onClick={onSwitchToLogin} className="button button--link">
                    Log in
                  </button>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupForm;