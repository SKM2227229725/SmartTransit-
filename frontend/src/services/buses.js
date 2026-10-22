import api from "./api";

export const busesService = {
  async list(params = {}) {
    const { data } = await api.get("/buses/", { params });
    return data;
  },
  async active() {
    const { data } = await api.get("/buses/active/");
    return data;
  },
  async detail(id) {
    const { data } = await api.get(`/buses/${id}/`);
    return data;
  },
  async location(id) {
    const { data } = await api.get(`/buses/${id}/location/`);
    return data;
  },
};

export const routesService = {
  async list() {
    const { data } = await api.get("/routes/"); // ✅ FIXED URL
    return data;
  },
  async detail(id) {
    const { data } = await api.get(`/routes/${id}/`); // ✅ FIXED URL
    return data;
  },
  async stops(routeId) {
    const { data } = await api.get(`/routes/${routeId}/stops/`); // ✅ FIXED URL
    return data;
  },
};

export const stopsService = {
  async list() {
    const { data } = await api.get("/stops/");
    return data;
  },
};