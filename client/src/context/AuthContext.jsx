import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [username, setUsername] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchUserData(token);
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUserData = async (token) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/checkAuth', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const userData = await response.json();
      setUsername(userData);
    } catch (error) {
        console.log(error)
        logout();
    } finally {
      setLoading(false);
    }
  };

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    setToken(token);
    setUsername(userData);
  };

  const signup = (token, userData) => {
    localStorage.setItem('token', token);
    setToken(token);
    setUsername(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUsername(null);
  };

  return (
    <AuthContext.Provider value={{ username, token, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);