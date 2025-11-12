import { AuthProvider } from './context/AuthContext.jsx'
import { BrowserRouter, Route, Routes } from "react-router";
import LoginPage from './pages/LoginPage.jsx'
import SignUpPage from './pages/SignUpPage';
import ProtectedRoute from './pages/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import WorkoutsPage from './pages/WorkoutsPage';
import NewWorkout from './pages/NewWorkout'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/workouts" element={<ProtectedRoute><WorkoutsPage /></ProtectedRoute>} />
          <Route path="/train" element={<ProtectedRoute><NewWorkout /></ProtectedRoute>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUpPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App