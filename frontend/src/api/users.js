import api from "@/api";

export const AuthAPI = {
  async login(userData) {
    return await api.post("auth/login", userData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },

  async register(userData) {
    return await api.post("auth/register", userData);
  },

  async logout() {
    return await api.post("auth/logout");
  },

  async getMe() {
    return await api.get("/users/me");
  },

  async requestVerifyToken(email) {
    return await api.post("/auth/request-verify-token", email);
  },

  async verifyToken(token) {
    return await api.post("/auth/verify", token);
  },
};
