import { SignupForm } from "@/components/SignUpFrom"
import { useAuth } from "@/context/AuthContext";


export default function SignUpPage() {
    const { signup } = useAuth();
        const handleSignup = async (formData) => {
        console.log('Signup data:', formData);
        try {
          const response = await fetch('http://127.0.0.1:8000/signup', {
            method: 'POST',
            body: formData
          });
          if(response.ok){
            const json_response = await response.json()
            const token = json_response.token.access_token
            const user = json_response["user"]
            signup(token, user)
          }
        } catch (error) {
          console.error(error);
        }
      };
  return (
    <div 
      className="flex min-h-svh w-full items-center justify-center p-6 md:p-10 bg-cover  bg-no-repeat bg-[url(/images/background.jpg)]" 
    >
      <div className="w-full max-w-sm">
        <SignupForm onSubmit={handleSignup} />
      </div>
    </div>
  )
}
