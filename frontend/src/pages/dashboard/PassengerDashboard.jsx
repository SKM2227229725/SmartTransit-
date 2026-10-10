import { useCallback, useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";

import MapView from "../../components/MapView";
import StopSelector from "../../components/StopSelector";
import ArrivalsPanel from "../../components/ArrivalsPanel";
import BusDetailsPanel from "../../components/BusDetailsPanel";
import { busesService, routesService, stopsService } from "../../services/buses";
import { usePolling } from "../../hooks/usePolling";

function haversineKm(lat1, lng1, lat2, lng2) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

export default function PassengerDashboard() {
  const [stops, setStops] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [routePolyline, setRoutePolyline] = useState([]);
  const [selectedStop, setSelectedStop] = useState(null);
  const [selectedBus, setSelectedBus] = useState(null);
  const [search, setSearch] = useState("");

  // Load stops + routes once
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [stopsRes, routesRes] = await Promise.all([
          stopsService.list(),
          routesService.list(),
        ]);
        if (!alive) return;
        const stopArr = Array.isArray(stopsRes.results)
          ? stopsRes.results
          : Array.isArray(stopsRes)
          ? stopsRes
          : [];
        const routeArr = Array.isArray(routesRes.results)
          ? routesRes.results
          : Array.isArray(routesRes)
          ? routesRes
          : [];
        setStops(stopArr);
        setRoutes(routeArr);

        if (routeArr.length > 0) {
          const stopsRes2 = await routesService.stops(routeArr[0].id);
          if (!alive) return;
          const ordered = Array.isArray(stopsRes2.data) ? stopsRes2.data : [];
          setRoutePolyline(
            ordered
              .map((rs) =>
                rs?.stop ? [rs.stop.latitude, rs.stop.longitude] : null
              )
              .filter(Boolean)
          );
        }
      } catch (e) {
        toast.error("Failed to load stops/routes.");
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  // Poll active buses
  const fetchActive = useCallback(async () => {
    const res = await busesService.active();
    return Array.isArray(res?.data) ? res.data : [];
  }, []);

  const { data: activeBuses = [], error: pollError } = usePolling(fetchActive, {
    interval: 5000,
  });

  // Ensure activeBuses is always an array
  const safeActiveBuses = Array.isArray(activeBuses) ? activeBuses : [];

  useEffect(() => {
    if (pollError) {
      toast.error("Connection lost. Retrying...");
    }
  }, [pollError]);

  // Filter buses by search
  const visibleBuses = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return safeActiveBuses;
    return safeActiveBuses.filter((b) => {
      const num = (b.bus_number || "").toLowerCase();
      const route = (b.route_code || b.route?.route_code || "").toLowerCase();
      return num.includes(q) || route.includes(q);
    });
  }, [safeActiveBuses, search]);

  // Compute arrivals for selected stop
  const arrivals = useMemo(() => {
    if (!selectedStop) return [];
    const results = [];
    safeActiveBuses.forEach((b) => {
      const lat = b.latitude ?? b.lat;
      const lng = b.longitude ?? b.lng;
      if (lat == null || lng == null) return;
      const distKm = haversineKm(lat, lng, selectedStop.latitude, selectedStop.longitude);
      const speed = b.speed && b.speed > 2 ? b.speed : 20;
      const etaMinutes = (distKm / speed) * 60;
      results.push({
        bus_id: b.bus_id || b.id,
        bus_number: b.bus_number || `Bus ${b.bus_id || b.id}`,
        eta_minutes: etaMinutes,
        distance_km: distKm,
      });
    });
    return results.sort((a, b) => a.eta_minutes - b.eta_minutes).slice(0, 5);
  }, [safeActiveBuses, selectedStop]);

  return (
    <div className="flex h-[calc(100vh-120px)] flex-col md:flex-row">
      {/* Sidebar */}
      <aside className="w-full overflow-y-auto border-r border-dark-border bg-dark-surface p-4 md:w-80 md:flex-shrink-0">
        <div className="mb-4">
          <input
            className="input"
            placeholder="Search bus or route..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <ArrivalsPanel stopName={selectedStop?.name} arrivals={arrivals} />

        <div className="mt-4">
          <StopSelector
            stops={stops}
            selectedStopId={selectedStop?.id}
            onSelect={setSelectedStop}
          />
        </div>
      </aside>

      {/* Map */}
      <section className="relative flex-1">
        <div className="absolute right-4 top-4 z-[999] flex items-center gap-2 rounded-full bg-dark-surface/90 px-3 py-1.5 text-xs shadow-lg">
          <span
            className={`h-2 w-2 rounded-full ${
              pollError ? "bg-red-500" : "bg-brand-green animate-pulse"
            }`}
          />
          <span>{pollError ? "Disconnected" : "Connected"}</span>
        </div>

        <BusDetailsPanel bus={selectedBus} onClose={() => setSelectedBus(null)} />

        <MapView
          buses={visibleBuses}
          stops={stops}
          routePolyline={routePolyline}
          selectedBusId={selectedBus?.bus_id || selectedBus?.id}
          onSelectBus={setSelectedBus}
          onSelectStop={setSelectedStop}
        />

        {(visibleBuses?.length ?? 0) === 0 && (
          <div className="pointer-events-none absolute inset-x-0 bottom-6 z-[999] flex justify-center">
            <div className="rounded-md bg-dark-surface/90 px-4 py-2 text-sm text-slate-300 shadow-lg">
              No active buses right now.
            </div>
          </div>
        )}
      </section>
    </div>
  );
}