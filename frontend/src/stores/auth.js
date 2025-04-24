import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  actions: {
    async login(credentials) {
      try {
        const response = await api.post('auth/login', credentials)
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        await this.fetchUser()
      } catch (error) {
        throw error.response?.data?.detail || 'Ошибка входа'
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

