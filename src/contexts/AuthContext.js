import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

// Define the provider component
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on initial load using localStorage
    const userData = localStorage.getItem('user_data');
    if (userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
    setLoading(false);
  }, []);

  const login = (email, password) => {
    // For demo purposes, we'll check if user exists in localStorage
    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]');
    const foundUser = storedUsers.find(user => user.email === email && user.password === password);

    if (foundUser) {
      // Remove password from user object for security
      const { password, ...userWithoutPassword } = foundUser;
      localStorage.setItem('user_data', JSON.stringify(userWithoutPassword));
      setUser(userWithoutPassword);
      return { success: true, user: userWithoutPassword };
    } else {
      return { success: false, error: 'Invalid email or password' };
    }
  };

  const signup = (userData) => {
    // Check if user already exists
    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]');
    const existingUser = storedUsers.find(user => user.email === userData.email);

    if (existingUser) {
      return { success: false, error: 'User already exists' };
    }

    // Add new user with background and preferences
    const newUser = {
      id: Date.now().toString(),
      ...userData,
      createdAt: new Date().toISOString()
    };

    storedUsers.push(newUser);
    localStorage.setItem('users', JSON.stringify(storedUsers));

    // Remove password from user object for security
    const { password, ...userWithoutPassword } = newUser;
    localStorage.setItem('user_data', JSON.stringify(userWithoutPassword));
    setUser(userWithoutPassword);

    return { success: true, user: userWithoutPassword };
  };

  const logout = () => {
    localStorage.removeItem('user_data');
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Create the hook separately
const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Export the provider and hook as named exports
export { AuthProvider, useAuth };

// Export the provider as default
export default AuthProvider;