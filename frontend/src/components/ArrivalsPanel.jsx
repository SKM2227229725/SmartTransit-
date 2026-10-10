export default function ArrivalsPanel({ stopName, arrivals }) {
  return (
    <div className="rounded-lg bg-gradient-to-br from-purple-600/80 via-purple-500/60 to-indigo-500/60 p-4 shadow-lg">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-white/80">
          Arrivals
        </h3>
        <span className="rounded-full bg-white/20 px-2 py-0.5 text-xs text-white">
          Live
        </span>
      </div>
      <p className="mt-1 text-sm font-medium text-white">{stopName || "Select a stop"}</p>

      <ul className="mt-3 space-y-2">
        {(!arrivals || arrivals.length === 0) && (
          <li className="text-xs text-white/70">No upcoming buses.</li>
        )}
        {arrivals?.map((a) => (
          <li
            key={a.bus_id}
            className="flex items-center justify-between rounded-md bg-black/20 px-3 py-2 text-sm text-white"
          >
            <span className="font-medium">{a.bus_number}</span>
            <span className="text-brand-orange font-semibold">
              {a.eta_minutes != null ? `${Math.round(a.eta_minutes)} min` : "—"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}