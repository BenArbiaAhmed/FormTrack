import { LoginForm } from "../components/LoginForm";
import { useAuth } from "../context/AuthContext";
export default function LoginPage() {


    const { login } = useAuth();
    const handleLogin = async (formData) => {
    console.log('Login data:', formData);
    try {
      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        body: formData
      });
      
      const json_response = await response.json()
      const token = json_response.token.access_token
      const user = json_response.user
      login(token, user)
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