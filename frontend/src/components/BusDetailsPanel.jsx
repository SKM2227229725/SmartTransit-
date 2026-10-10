import { formatDistance } from "../utils/formatters";

export default function BusDetailsPanel({ bus, onClose }) {
  if (!bus) return null;

  const statusColor =
    bus.status === "active"
      ? "bg-brand-green"
      : bus.status === "delayed"
      ? "bg-amber-500"
      : "bg-slate-500";

  return (
    <div className="absolute right-4 top-4 z-[1000] w-72 rounded-lg border border-dark-border bg-dark-surface/95 p-4 shadow-2xl backdrop-blur">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold">{bus.bus_number}</h3>
          {bus.route_code && (
            <p className="text-xs text-slate-400">Route {bus.route_code}</p>
          )}
        </div>
        <button
          onClick={onClose}
          className="rounded-md px-2 py-1 text-slate-400 hover:bg-slate-700 hover:text-white"
        >
          ✕
        </button>
      </div>

      <div className="mt-4 space-y-2 text-sm">
        <Row label="Status">
          <span className="inline-flex items-center gap-1.5">
            <span className={`h-2 w-2 rounded-full ${statusColor}`} />
            <span className="capitalize">{bus.status || "unknown"}</span>
          </span>
        </Row>
        <Row label="Speed">
          {bus.speed != null ? `${Number(bus.speed).toFixed(1)} km/h` : "—"}
        </Row>
        {bus.next_stop && <Row label="Next stop">{bus.next_stop}</Row>}
        {bus.eta_minutes != null && (
          <Row label="ETA">
            <span className="font-semibold text-brand-orange">
              {Math.round(bus.eta_minutes)} min
            </span>
          </Row>
        )}
        {bus.distance_km != null && (
          <Row label="Distance">{formatDistance(bus.distance_km)}</Row>
        )}
      </div>
    </div>
  );
}

function Row({ label, children }) {
  return (
    <div className="flex items-center justify-between border-t border-dark-border/50 py-1.5">
      <span className="text-xs uppercase tracking-wide text-slate-500">{label}</span>
      <span className="text-slate-200">{children}</span>
    </div>
  );
}