import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import ErrorMessage from "../../components/ErrorMessage";
import { useAuth } from "../../hooks/useAuth";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const onChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const data = await login(form);
      toast.success(`Welcome back, ${data.user.email}`);
      const role = data.user.role;
      navigate(`/${role}/dashboard`, { replace: true });
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Login failed. Check your credentials.";
      setError(msg);
      toast.error(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto flex max-w-md flex-col px-6 py-16">
      <h1 className="text-2xl font-semibold">Welcome back</h1>
      <p className="mt-1 text-sm text-slate-400">
        Sign in to your SmartTransit account.
      </p>

      <form onSubmit={onSubmit} className="mt-8 space-y-4">
        <ErrorMessage message={error} />

        <div>
          <label className="mb-1 block text-xs text-slate-400">Email</label>
          <input
            className="input"
            type="email"
            name="email"
            value={form.email}
            onChange={onChange}
            required
            autoComplete="email"
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-400">Password</label>
          <input
            className="input"
            type="password"
            name="password"
            value={form.password}
            onChange={onChange}
            required
            autoComplete="current-password"
          />
        </div>

        <button className="btn-primary w-full" disabled={submitting}>
          {submitting ? "Signing in..." : "Sign in"}
        </button>
      </form>

      <p className="mt-6 text-sm text-slate-400">
        New here?{" "}
        <Link to="/register" className="text-brand-orange hover:underline">
          Create an account
        </Link>
      </p>
    </div>
  );
}