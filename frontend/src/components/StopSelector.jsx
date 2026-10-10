export default function StopSelector({ stops, selectedStopId, onSelect }) {
  return (
    <div className="mb-4">
      <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
        Bus Stops
      </label>
      <ul className="space-y-1">
        {stops.length === 0 && (
          <li className="text-xs text-slate-500">No stops available.</li>
        )}
        {stops.map((s) => {
          const active = s.id === selectedStopId;
          return (
            <li key={s.id}>
              <button
                type="button"
                onClick={() => onSelect(s)}
                className={`w-full rounded-md px-3 py-2 text-left text-sm transition-colors ${
                  active
                    ? "bg-brand-orange/20 text-brand-orange ring-1 ring-brand-orange/40"
                    : "text-slate-300 hover:bg-slate-700/40"
                }`}
              >
                <div className="flex items-center gap-2">
                  <span className="h-2 w-2 flex-shrink-0 rounded-full bg-brand-green" />
                  <span className="truncate">{s.name}</span>
                </div>
                {s.landmark && (
                  <p className="ml-4 mt-0.5 truncate text-xs text-slate-500">
                    {s.landmark}
                  </p>
                )}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}