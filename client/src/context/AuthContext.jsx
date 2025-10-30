import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));


  const verifyToken = async () => {
    if (!token) return false;
    
    try {
      const response = await fetch('http://127.0.0.1:8000/checkAuth', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (!response.ok) {
        logout();
        return false;
      }
      
      const userData = await response.json();
      setUser(userData);
      return true;
    } catch (error) {
      console.log(error);
      logout();
      return false;
    }
  };

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    setToken(token);
    setUser(userData);
  };

  const signup = (token, userData) => {
    localStorage.setItem('token', token);
    setToken(token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, verifyToken, signup }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);