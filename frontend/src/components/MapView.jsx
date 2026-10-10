import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";

import BusMarker from "./BusMarker";

// Solapur center
const DEFAULT_CENTER = [17.6599, 75.9064];
const DEFAULT_ZOOM = 13;

const stopIcon = new L.DivIcon({
  className: "",
  html: `<div style="width:14px;height:14px;border-radius:50%;background:#22c55e;border:2px solid #fff;box-shadow:0 0 4px rgba(0,0,0,.6);"></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7],
});

export default function MapView({
  buses = [],
  stops = [],
  routePolyline = [],
  selectedBusId,
  onSelectBus,
  onSelectStop,
}) {
  return (
    <MapContainer
      center={DEFAULT_CENTER}
      zoom={DEFAULT_ZOOM}
      style={{ height: "100%", width: "100%" }}
      scrollWheelZoom
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Route polyline (orange) */}
      {routePolyline.length > 1 && (
        <Polyline
          positions={routePolyline}
          pathOptions={{ color: "#f97316", weight: 4, opacity: 0.85 }}
        />
      )}

      {/* Stop markers (green) */}
      {stops.map((s) => (
        <Marker
          key={`stop-${s.id}`}
          position={[s.latitude, s.longitude]}
          icon={stopIcon}
          eventHandlers={{
            click: () => onSelectStop && onSelectStop(s),
          }}
        >
          <Popup>
            <strong>{s.name}</strong>
            {s.landmark && (
              <>
                <br />
                <span style={{ opacity: 0.7, fontSize: 12 }}>{s.landmark}</span>
              </>
            )}
          </Popup>
        </Marker>
      ))}

      {/* Bus markers (orange) */}
      {buses.map((b) => (
        <BusMarker
          key={`bus-${b.bus_id || b.id}`}
          bus={b}
          isSelected={(b.bus_id || b.id) === selectedBusId}
          onClick={() => onSelectBus && onSelectBus(b)}
        />
      ))}
    </MapContainer>
  );
}