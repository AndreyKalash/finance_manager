import { defineStore } from "pinia";
import { AuthAPI } from "@/api/users";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: localStorage.getItem("token") || null,
  }),
  actions: {
    async login({ username, password }) {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      try {
        const response = await AuthAPI.login(params);
        this.token = response.data.access_token;
        localStorage.setItem("token", this.token);
        await this.fetchUser();
        return response;
      } catch (error) {
        throw error.response?.data?.detail || "Ошибка входа";
      }
    },
    async initAuth() {
      if (this.token != 'undefined' && !this.user) {
        try {
          await this.fetchUser();
        } catch (error) {
          // await this.logout();
        }
      }
    },
    async register(userData) {
      try {
        const response = await AuthAPI.register(userData);
        if (response.data.access_token) {
          this.token = response.data.access_token;
          localStorage.setItem("token", this.token);
        }

        return response;
      } catch (error) {
        throw error.response?.data?.detail || "Ошибка регистрации";
      }
    },
    async fetchUser() {
      const response = await AuthAPI.getMe();
      this.user = response.data;
    },
    async logout() {
      this.user = null;
      this.token = null;
      // await AuthAPI.logout()
      localStorage.removeItem("token");
    },
    async requestToken(email) {
      return await AuthAPI.requestVerifyToken(email);
    },
    async verifyToken(token) {
      return await AuthAPI.verifyToken(token);
    },
  },
});
