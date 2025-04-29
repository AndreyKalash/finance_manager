import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: process.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
  // headers: {
  //   'Content-Type': 'application/json'
  // }
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
    const token = response.headers['authorization']
    if (token) {
      const authStore = useAuthStore()
      authStore.token = token.split(' ')[1];
      localStorage.setItem('token', authStore.token)
    }
    return response
  },
  error => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      router.push('/login')
    }
    if (error.message.includes('CORS')) {
      alert('Ошибка CORS: проверьте настройки сервера');
    }
    return Promise.reject(error)
  }
);

export default api