import { StrictMode } from 'react'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { BrowserRouter, Route, Routes } from "react-router";
import ReactDOM from "react-dom/client";
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import ProtectedRoute from './pages/ProtectedRoute';

const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          
          {/* <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          /> */}
        </Routes>
      </BrowserRouter>
    </AuthProvider>
)
