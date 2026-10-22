import api from "./api";

export const driverService = {
  async myTrips() {
    const { data } = await api.get("/trips/my/");
    return data;
  },

  async activeTrip() {
    const { data } = await api.get("/trips/active/");
    return data;
  },

  async startTrip(busId, routeId) {
    const { data } = await api.post("/trips/start/", {
      bus_id: busId,
      route_id: routeId,
    });
    return data;
  },

  async endTrip(tripId) {
    const { data } = await api.post(`/trips/${tripId}/end/`);
    return data;
  },

  async sendLocation(tripId, busId, latitude, longitude, speed, heading) {
    const { data } = await api.post("/location/update/", {
      trip: tripId,
      bus: busId,
      latitude,
      longitude,
      speed,
      heading,
      source: "simulator",
    });
    return data;
  },
};