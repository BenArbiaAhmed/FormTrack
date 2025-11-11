import { LoginForm } from "../components/LoginForm";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router";
import axios from '../axios/axiosInstance'
export default function LoginPage() {
    let navigate = useNavigate();
    const { login } = useAuth();
    const handleLogin = async (formData) => {
    console.log('Login data:', formData);
    try {
      const response = await axios.post('/login', formData);  
      const json_response = response.data
      const token = json_response.token.access_token
      const user = json_response.user
      login(token, user)
      navigate("/dashboard")
      
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <div 
      className="flex min-h-svh w-full items-center justify-center p-6 md:p-10 bg-cover  bg-no-repeat bg-[url(/images/background.jpg)]" 
    >
      <div className="w-full max-w-sm">
        <LoginForm onSubmit={handleLogin} />
      </div>
    </div>
  )
}