import { Navigate } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { useEffect, useState } from 'react';

function ProtectedRoute({ children }) {
  const { user, token, verifyToken } = useAuth();
  const [isVerifying, setIsVerifying] = useState(true);

  useEffect(() => {
    const verify = async () => {
      if (token && !user) {
        await verifyToken();
      }
      setIsVerifying(false);
    };
    
    verify();
  }, [token, user, verifyToken]);

  if (isVerifying) {
    return <div>Loading...</div>;
  }

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;