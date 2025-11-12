import axios from 'axios'
const token = localStorage.getItem("token")
const instance = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 1000,
  headers: {
    Authorization: `Bearer ${token}`
  }
});

instance.interceptors.request.use(
  (config) => {
        const publicRoutes = ['/login', '/signup'];
    
    
    const isPublicRoute = publicRoutes.some(route => 
      config.url.includes(route)
    );
    
    
    if (!isPublicRoute) {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance