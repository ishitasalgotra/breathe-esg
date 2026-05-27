const toneClasses = {
  emerald: "border-emerald-200 bg-emerald-50 text-emerald-700",
  slate: "border-slate-200 bg-slate-100 text-slate-700",
  zinc: "border-zinc-200 bg-zinc-100 text-zinc-700",
  amber: "border-amber-200 bg-amber-50 text-amber-800",
  rose: "border-rose-200 bg-rose-50 text-rose-700",
};

const statusTones = {
  approved: "emerald",
  processed: "emerald",
  completed: "emerald",
  success: "emerald",
  clear: "emerald",
  pending: "amber",
  queued: "amber",
  processing: "slate",
  flagged: "amber",
  rejected: "rose",
  failed: "rose",
  error: "rose",
};

function labelFor(value) {
  if (value === true) return "Flagged";
  if (value === false) return "Clear";
  return String(value || "Unknown").replaceAll("_", " ");
}

export default function Badge({ children, value, tone, className = "" }) {
  const label = children || labelFor(value);
  const resolvedTone = tone || statusTones[String(value).toLowerCase()] || "zinc";
  return <span className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold capitalize leading-none ${toneClasses[resolvedTone]} ${className}`}>{label}</span>;
}
