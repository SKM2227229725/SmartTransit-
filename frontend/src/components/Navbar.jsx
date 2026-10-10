import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const dashboardPath = user ? `/${user.role}/dashboard` : "/login";

  return (
    <nav className="border-b border-dark-border bg-dark-surface">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-lg font-semibold">
          <span className="text-brand-orange">🚌</span>
          <span>SmartTransit</span>
        </Link>

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <Link to={dashboardPath} className="btn-ghost text-sm">
                Dashboard
              </Link>
              <span className="hidden text-xs text-slate-400 sm:inline">
                {user?.email} · {user?.role}
              </span>
              <button className="btn-secondary text-sm" onClick={handleLogout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-ghost text-sm">
                Login
              </Link>
              <Link to="/register" className="btn-primary text-sm">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}