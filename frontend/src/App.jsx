import { Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import LandingPage from "./pages/LandingPage";
import NotFound from "./pages/NotFound";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import PassengerDashboard from "./pages/dashboard/PassengerDashboard";
import DriverDashboard from "./pages/dashboard/DriverDashboard";
import AuthorityDashboard from "./pages/dashboard/AuthorityDashboard";

export default function App() {
  return (
    <div className="flex min-h-full flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route element={<ProtectedRoute allowedRoles={["passenger"]} />}>
            <Route path="/passenger/dashboard" element={<PassengerDashboard />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={["driver"]} />}>
            <Route path="/driver/dashboard" element={<DriverDashboard />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={["authority"]} />}>
            <Route path="/authority/dashboard" element={<AuthorityDashboard />} />
          </Route>

          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <footer className="border-t border-dark-border bg-dark-surface px-4 py-3 text-center text-xs text-slate-500">
        SmartTransit · AI-powered real-time public transport tracking
      </footer>
    </div>
  );
}