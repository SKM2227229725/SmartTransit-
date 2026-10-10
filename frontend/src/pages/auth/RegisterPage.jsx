import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import ErrorMessage from "../../components/ErrorMessage";
import { useAuth } from "../../hooks/useAuth";

const initial = {
  email: "",
  full_name: "",
  phone: "",
  role: "passenger",
  password: "",
  password_confirm: "",
};

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(initial);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const onChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setFieldErrors({});
    setSubmitting(true);
    try {
      await register(form);
      toast.success("Registration successful! Please sign in.");
      navigate("/login", { replace: true });
    } catch (err) {
      const data = err.response?.data;
      if (data?.errors && typeof data.errors === "object") {
        setFieldErrors(data.errors);
      }
      setError(data?.message || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  };

  const fieldError = (name) =>
    fieldErrors[name]?.[0] || fieldErrors[name] || "";

  return (
    <div className="mx-auto flex max-w-md flex-col px-6 py-16">
      <h1 className="text-2xl font-semibold">Create your account</h1>
      <p className="mt-1 text-sm text-slate-400">
        Register as a passenger or a driver.
      </p>

      <form onSubmit={onSubmit} className="mt-8 space-y-4">
        <ErrorMessage message={error} />

        <div>
          <label className="mb-1 block text-xs text-slate-400">Email *</label>
          <input
            className="input"
            type="email"
            name="email"
            value={form.email}
            onChange={onChange}
            required
          />
          {fieldError("email") && (
            <p className="mt-1 text-xs text-red-400">{fieldError("email")}</p>
          )}
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-400">Full name</label>
          <input
            className="input"
            name="full_name"
            value={form.full_name}
            onChange={onChange}
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-400">Phone</label>
          <input
            className="input"
            name="phone"
            value={form.phone}
            onChange={onChange}
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-400">Role *</label>
          <select
            className="input"
            name="role"
            value={form.role}
            onChange={onChange}
          >
            <option value="passenger">Passenger</option>
            <option value="driver">Driver</option>
          </select>
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-400">Password *</label>
          <input
            className="input"
            type="password"
            name="password"
            value={form.password}
            onChange={onChange}
            required
          />
          {fieldError("password") && (
            <p className="mt-1 text-xs text-red-400">{fieldError("password")}</p>
          )}
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-400">
            Confirm password *
          </label>
          <input
            className="input"
            type="password"
            name="password_confirm"
            value={form.password_confirm}
            onChange={onChange}
            required
          />
        </div>

        <button className="btn-primary w-full" disabled={submitting}>
          {submitting ? "Creating..." : "Create account"}
        </button>
      </form>

      <p className="mt-6 text-sm text-slate-400">
        Already registered?{" "}
        <Link to="/login" className="text-brand-orange hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}