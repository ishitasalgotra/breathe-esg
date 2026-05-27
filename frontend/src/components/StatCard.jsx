import Card from "./Card";

export default function StatCard({ label, value, icon: Icon, tone = "emerald" }) {
  const tones = {
    emerald: "bg-emerald-50 text-emerald-700 ring-emerald-100",
    slate: "bg-slate-100 text-slate-700 ring-slate-200",
    zinc: "bg-zinc-100 text-zinc-700 ring-zinc-200",
    amber: "bg-amber-50 text-amber-700 ring-amber-100",
  };
  return <Card className="p-5 hover:-translate-y-1 hover:shadow-soft"><div className="flex items-start justify-between gap-4"><div><div className="text-sm font-medium text-slate-500">{label}</div><div className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">{value ?? "-"}</div></div>{Icon && <div className={`grid h-11 w-11 shrink-0 place-items-center rounded-xl ring-1 ${tones[tone]}`}><Icon size={21}/></div>}</div></Card>;
}
