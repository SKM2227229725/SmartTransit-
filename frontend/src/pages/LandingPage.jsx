import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function LandingPage() {
  const { isAuthenticated, user } = useAuth();
  const dashboardPath = user ? `/${user.role}/dashboard` : "/login";

  return (
    <div className="mx-auto max-w-5xl px-6 py-20 text-center">
      <span className="rounded-full border border-brand-orange/40 bg-brand-orange/10 px-3 py-1 text-xs text-brand-orange">
        Smart City · Real-time Bus Tracking
      </span>
      <h1 className="mt-6 text-4xl font-bold tracking-tight sm:text-5xl">
        Track buses in <span className="text-brand-orange">real time</span>.
        <br />
        Never miss your ride again.
      </h1>
      <p className="mx-auto mt-6 max-w-2xl text-slate-400">
        SmartTransit brings AI-powered ETA prediction, live GPS tracking, and
        smart route optimization to small cities — starting with Solapur.
      </p>

      <div className="mt-10 flex justify-center gap-4">
        {isAuthenticated ? (
          <Link to={dashboardPath} className="btn-primary">
            Open Dashboard
          </Link>
        ) : (
          <>
            <Link to="/login" className="btn-primary">
              Sign in
            </Link>
            <Link to="/register" className="btn-secondary">
              Create account
            </Link>
          </>
        )}
      </div>

      <div className="mt-20 grid gap-6 sm:grid-cols-3">
        <Feature icon="📍" title="Live Tracking" text="See buses move on the map in real time." />
        <Feature icon="🤖" title="AI ETA" text="Machine learning predicts arrival times." />
        <Feature icon="📊" title="Analytics" text="Authority dashboards with rich insights." />
      </div>
    </div>
  );
}

function Feature({ icon, title, text }) {
  return (
    <div className="card text-left">
      <div className="text-3xl">{icon}</div>
      <h3 className="mt-3 text-lg font-semibold">{title}</h3>
      <p className="mt-1 text-sm text-slate-400">{text}</p>
    </div>
  );
}