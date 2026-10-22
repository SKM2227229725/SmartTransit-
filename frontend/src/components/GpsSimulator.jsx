import { useEffect, useRef, useState } from "react";
import toast from "react-hot-toast";

import { driverService } from "../services/driver";

/**
 * Simulates a bus moving along a route, sending GPS pings every 5 seconds.
 */
export default function GpsSimulator({ trip, routeStops, isActive, onPing }) {
  const [isRunning, setIsRunning] = useState(false);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [progress, setProgress] = useState(0);
  const [currentLat, setCurrentLat] = useState(null);
  const [currentLng, setCurrentLng] = useState(null);
  const intervalRef = useRef(null);

  // Initialize position from first stop
  useEffect(() => {
    if (routeStops?.length > 0 && currentLat === null) {
      setCurrentLat(routeStops[0].stop.latitude);
      setCurrentLng(routeStops[0].stop.longitude);
    }
  }, [routeStops, currentLat]);

  const moveToNextStop = () => {
    if (!routeStops || routeStops.length < 2) return;

    if (currentIdx >= routeStops.length - 1) {
      // loop back
      setCurrentIdx(0);
      setProgress(0);
      return;
    }

    const from = routeStops[currentIdx].stop;
    const to = routeStops[currentIdx + 1].stop;
    const nextProgress = progress + 0.1;

    if (nextProgress >= 1) {
      setCurrentIdx(currentIdx + 1);
      setProgress(0);
      setCurrentLat(to.latitude);
      setCurrentLng(to.longitude);
    } else {
      // interpolate between stops
      const lat = from.latitude + (to.latitude - from.latitude) * nextProgress;
      const lng = from.longitude + (to.longitude - from.longitude) * nextProgress;
      setProgress(nextProgress);
      setCurrentLat(lat);
      setCurrentLng(lng);
    }
  };

  const sendPing = async () => {
    if (!trip || currentLat === null || currentLng === null) return;
    try {
      const speed = 20 + Math.random() * 15;
      const heading = Math.random() * 360;
      await driverService.sendLocation(
        trip.id,
        trip.bus?.id || trip.bus,
        currentLat,
        currentLng,
        speed,
        heading
      );
      if (onPing) onPing({ lat: currentLat, lng: currentLng, speed });
    } catch (err) {
      console.error("GPS ping failed:", err);
    }
  };

  useEffect(() => {
    if (!isRunning || !isActive) {
      if (intervalRef.current) clearInterval(intervalRef.current);
      return;
    }

    intervalRef.current = setInterval(async () => {
      moveToNextStop();
      await sendPing();
    }, 5000); // every 5 seconds per spec

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isRunning, isActive, currentIdx, progress]);

  const handleStart = () => {
    setIsRunning(true);
    toast.success("GPS Simulator started — pinging every 5s");
  };

  const handleStop = () => {
    setIsRunning(false);
    toast("GPS Simulator stopped");
  };

  if (!trip) {
    return (
      <div className="card text-center text-slate-400">
        Start a trip to enable GPS simulation.
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
          GPS Simulator
        </h3>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs ${
            isRunning
              ? "bg-brand-green/20 text-brand-green"
              : "bg-slate-700 text-slate-300"
          }`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              isRunning ? "bg-brand-green animate-pulse" : "bg-slate-500"
            }`}
          />
          {isRunning ? "Transmitting" : "Idle"}
        </span>
      </div>

      <div className="mt-4 space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-slate-500">Latitude</span>
          <span className="font-mono text-slate-200">
            {currentLat?.toFixed(6) ?? "—"}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Longitude</span>
          <span className="font-mono text-slate-200">
            {currentLng?.toFixed(6) ?? "—"}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Next Stop</span>
          <span className="text-slate-200">
            {routeStops?.[currentIdx + 1]?.stop?.name || "End of route"}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Progress</span>
          <span className="text-slate-200">
            Stop {(currentIdx + 1)} / {routeStops?.length ?? 0}
          </span>
        </div>
      </div>

      <div className="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-slate-700">
        <div
          className="h-full bg-brand-orange transition-all duration-1000"
          style={{ width: `${progress * 100}%` }}
        />
      </div>

      <div className="mt-4 flex gap-2">
        {!isRunning ? (
          <button className="btn-primary flex-1" onClick={handleStart}>
            ▶ Start GPS
          </button>
        ) : (
          <button className="btn-secondary flex-1" onClick={handleStop}>
            ⏸ Stop GPS
          </button>
        )}
      </div>
    </div>
  );
}