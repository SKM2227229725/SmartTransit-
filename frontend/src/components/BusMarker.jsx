import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

function makeBusIcon(isSelected) {
  const size = isSelected ? 44 : 38;
  const glow = isSelected
    ? "0 0 0 6px rgba(249,115,22,0.35)"
    : "0 0 0 3px rgba(249,115,22,0.2)";
  return new L.DivIcon({
    className: "",
    html: `
      <div style="
        width:${size}px;height:${size}px;
        background:#f97316;border:3px solid #fff;border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        font-size:${isSelected ? 22 : 18}px;
        box-shadow:${glow};
      ">🚌</div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}

export default function BusMarker({ bus, isSelected, onClick }) {
  const lat = bus.latitude ?? bus.lat;
  const lng = bus.longitude ?? bus.lng;

  if (lat == null || lng == null) return null;

  return (
    <Marker
      position={[lat, lng]}
      icon={makeBusIcon(isSelected)}
      eventHandlers={{ click: onClick }}
    >
      <Popup>
        <strong>{bus.bus_number || `Bus #${bus.bus_id || bus.id}`}</strong>
        <br />
        Speed: {bus.speed != null ? `${Number(bus.speed).toFixed(1)} km/h` : "—"}
        <br />
        Status: {bus.status || "—"}
      </Popup>
    </Marker>
  );
}