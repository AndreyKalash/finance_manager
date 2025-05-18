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
    return api.post("auth/register", userData);
  },

  async logout() {
    return api.post("auth/logout");
  },

  async getMe() {
    return api.get("/users/me");
  },

  async requestVerifyToken(email) {
    return api.post("/auth/request-verify-token", email);
  },

  async verifyToken(token) {
    return api.post("/auth/verify", token);
  },
};
