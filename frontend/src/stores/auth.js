import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  actions: {
    async login({ username, password }) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      try {
        const response = await api.post('auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        // this.token = response.data.access_token
        // localStorage.setItem('token', this.token)
        await this.fetchUser()
        // console.log(response.data)
        return response
      } catch (error) {
        throw error.response?.data?.detail || 'Ошибка входа'
      }
    },
    async register({ email, username, password }) {
      try {
        const response = await api.post('/auth/register', {
          email,
          username,
          password
        });
        
        if (response.data.access_token) {
          this.token = response.data.access_token;
          localStorage.setItem('token', this.token);
        }
        
        return response;
      } catch (error) {
        throw error.response?.data?.detail || 'Ошибка регистрации';
      }
    }
    
    
    ,
    async fetchUser() {
      const response = await api.get('/users/me')
      this.user = response.data
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})

