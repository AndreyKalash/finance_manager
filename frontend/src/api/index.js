import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: process.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

api.interceptors.response.use(
  response => {
    const bodyToken = response.data?.access_token
    const headerToken = response.headers['authorization']
    
    if (bodyToken || headerToken) {
      const authStore = useAuthStore()
      const token = bodyToken || headerToken.split(' ')[1]
      
      authStore.token = token
      localStorage.setItem('token', token)
    }
    
    return response
  },
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
      }
      
      if (error.response.data?.detail?.includes('CORS')) {
        alert('Ошибка CORS: проверьте настройки сервера')
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
