import api from '@/api'

export const AuthService = {
  async login(userData) {
    return api.post('auth/login', userData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  async register(userData) {
    return api.post('auth/register', userData)
  },

  async logout() {
    return api.post('auth/logout')
  },

  async getMe() {
    return api.get('/users/me')
  }
}
