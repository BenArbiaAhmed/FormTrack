import './index.css'
import { AuthProvider } from './context/AuthContext.jsx'
import { BrowserRouter, Route, Routes } from "react-router";
import ReactDOM from "react-dom/client";
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import ProtectedRoute from './pages/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import WorkoutsPage from './pages/WorkoutsPage';
import NewWorout from './pages/NewWorkout'


const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard" element={<ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>} />
          <Route path="/workouts" element={<ProtectedRoute>
                <WorkoutsPage />
              </ProtectedRoute>} />
          <Route path="/newworkout" element={<ProtectedRoute>
                <NewWorout />
              </ProtectedRoute>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUpPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
)
