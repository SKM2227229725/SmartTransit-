export function formatDateTime(iso) {
  if (!iso) return "-";
  try {
    return new Date(iso).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso;
  }
}

export function formatDistance(km) {
  if (km == null) return "-";
  return `${Number(km).toFixed(2)} km`;
}

export function formatCurrency(amount) {
  if (amount == null) return "-";
  return `₹${Number(amount).toFixed(2)}`;
}