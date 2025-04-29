import { defineStore } from 'pinia'
import { AuthService } from '@/api/users'

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
        const response = await AuthService.login(formData)
        await this.fetchUser()
        return response
      } catch (error) {
        throw error.response?.data?.detail || 'Ошибка входа'
      }
    },
    async register(userData) {
      try {
        const response = await AuthService.register(userData);
        if (response.data.access_token) {
          this.token = response.data.access_token;
          localStorage.setItem('token', this.token);
        }
        
        return response;
      } catch (error) {
        throw error.response?.data?.detail || 'Ошибка регистрации';
      }
    },
    async fetchUser() {
      const response = await AuthService.getMe()
      this.user = response.data
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})

