import api from "./api";

export const authService = {
  async register(payload) {
    const { data } = await api.post("/auth/register/", payload);
    return data;
  },

  async login({ email, password }) {
    const { data } = await api.post("/auth/login/", { email, password });
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    localStorage.setItem("user", JSON.stringify(data.user));
    return data;
  },

  async profile() {
    const { data } = await api.get("/auth/profile/");
    return data;
  },

  async updateProfile(payload) {
    const { data } = await api.patch("/auth/profile/", payload);
    return data;
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  },

  getCurrentUser() {
    try {
      const raw = localStorage.getItem("user");
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  isAuthenticated() {
    return !!localStorage.getItem("access_token");
  },
};