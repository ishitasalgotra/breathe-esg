export default function Card({ children, className = "" }) {
  return <div className={`rounded-xl border border-slate-200 bg-white shadow-card transition duration-200 ${className}`}>{children}</div>;
}
