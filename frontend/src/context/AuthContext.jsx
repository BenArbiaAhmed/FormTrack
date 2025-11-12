import { createContext, useContext, useState } from 'react';
import axios from '../axios/axiosInstance'

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));


  const verifyToken = async () => {
    if (!token) return false;
    
    try {
      const response = await axios.get('/auth/checkAuth', {
        headers: { Authorization: `Bearer ${token}` } 
      });
      
      const userData = response.data
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