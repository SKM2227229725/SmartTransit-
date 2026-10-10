import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-md px-6 py-20 text-center">
      <h1 className="text-6xl font-bold text-brand-orange">404</h1>
      <p className="mt-4 text-slate-400">This page does not exist.</p>
      <Link to="/" className="btn-primary mt-8 inline-flex">
        Go home
      </Link>
    </div>
  );
}