import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import TripStatusCard from "../../components/TripStatusCard";
import GpsSimulator from "../../components/GpsSimulator";
import Loading from "../../components/Loading";
import { driverService } from "../../services/driver";
import { busesService, routesService } from "../../services/buses";

export default function DriverDashboard() {
  const [activeTrip, setActiveTrip] = useState(null);
  const [routeStops, setRouteStops] = useState([]);
  const [buses, setBuses] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [selectedBusId, setSelectedBusId] = useState("");
  const [selectedRouteId, setSelectedRouteId] = useState("");
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  // Load data
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [busRes, routeRes, activeRes] = await Promise.all([
          busesService.list(),
          routesService.list(),
          driverService.activeTrip(),
        ]);
        if (!alive) return;
        setBuses(busRes.results || busRes);
        setRoutes(routeRes.results || routeRes);

        const active = (activeRes.data || []).find(
          (t) => t.driver_email // any active
        );
        if (active) {
          setActiveTrip(active);
          const stopsRes = await routesService.stops(active.route.id);
          if (alive) setRouteStops(stopsRes.data || []);
        }
      } catch (err) {
        toast.error("Failed to load driver data");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const handleStartTrip = async () => {
    if (!selectedBusId || !selectedRouteId) {
      toast.error("Select both a bus and a route");
      return;
    }
    setStarting(true);
    try {
      const res = await driverService.startTrip(
        Number(selectedBusId),
        Number(selectedRouteId)
      );
      const trip = res.data;
      setActiveTrip(trip);
      const stopsRes = await routesService.stops(trip.route.id);
      setRouteStops(stopsRes.data || []);
      toast.success("Trip started!");
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        err.response?.data?.errors?.non_field_errors?.[0] ||
        "Could not start trip";
      toast.error(msg);
    } finally {
      setStarting(false);
    }
  };

  const handleEndTrip = async () => {
    if (!activeTrip) return;
    if (!confirm("End this trip? The bus will stop broadcasting.")) return;
    try {
      await driverService.endTrip(activeTrip.id);
      setActiveTrip(null);
      setRouteStops([]);
      toast.success("Trip ended");
    } catch (err) {
      toast.error("Failed to end trip");
    }
  };

  if (loading) return <Loading label="Loading driver console..." />;

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold">Driver Console</h1>
        <p className="text-sm text-slate-400">
          Manage your trip, broadcast GPS, and track live passenger counts.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Left: Active trip or start form */}
        <div className="space-y-4">
          {activeTrip ? (
            <>
              <TripStatusCard trip={activeTrip} />
              <button className="btn-secondary w-full" onClick={handleEndTrip}>
                End Trip
              </button>
            </>
          ) : (
            <div className="card">
              <h2 className="text-lg font-semibold">Start a new trip</h2>
              <p className="mt-1 text-xs text-slate-400">
                Select your assigned bus and route.
              </p>

              <div className="mt-4 space-y-3">
                <div>
                  <label className="mb-1 block text-xs text-slate-400">
                    Bus
                  </label>
                  <select
                    className="input"
                    value={selectedBusId}
                    onChange={(e) => setSelectedBusId(e.target.value)}
                  >
                    <option value="">Select a bus...</option>
                    {buses.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.bus_number} — {b.license_plate}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="mb-1 block text-xs text-slate-400">
                    Route
                  </label>
                  <select
                    className="input"
                    value={selectedRouteId}
                    onChange={(e) => setSelectedRouteId(e.target.value)}
                  >
                    <option value="">Select a route...</option>
                    {routes.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.route_code} — {r.name}
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  className="btn-primary w-full"
                  onClick={handleStartTrip}
                  disabled={starting}
                >
                  {starting ? "Starting..." : "▶ Start Trip"}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Right: GPS Simulator */}
        <div>
          <GpsSimulator
            trip={activeTrip}
            routeStops={routeStops}
            isActive={!!activeTrip}
          />
        </div>
      </div>
    </div>
  );
}