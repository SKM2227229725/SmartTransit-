import { formatDateTime } from "../utils/formatters";

export default function TripStatusCard({ trip }) {
  if (!trip) return null;

  const statusColor =
    trip.status === "active"
      ? "bg-brand-green"
      : trip.status === "paused"
      ? "bg-amber-500"
      : "bg-slate-500";

  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">
            Active Trip
          </p>
          <h3 className="text-xl font-semibold">
            {trip.bus?.bus_number || "Bus"}
          </h3>
          <p className="text-xs text-slate-400">
            Route {trip.route?.route_code} — {trip.route?.name}
          </p>
        </div>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full bg-slate-800 px-2 py-1 text-xs`}
        >
          <span className={`h-2 w-2 rounded-full ${statusColor}`} />
          {trip.status}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
        <Metric label="Started" value={formatDateTime(trip.started_at)} />
        <Metric label="Passengers" value={trip.total_passengers ?? 0} />
        <Metric
          label="Distance"
          value={`${Number(trip.distance_covered_km || 0).toFixed(2)} km`}
        />
        <Metric
          label="Trip ID"
          value={`#${String(trip.id).padStart(4, "0")}`}
        />
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="font-medium text-slate-200">{value}</p>
    </div>
  );
}