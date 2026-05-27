import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, Clock3, Database } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../api/client";
import Badge from "../components/Badge";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import PageLayout from "../components/PageLayout";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get("/emissions/records/dashboard/").then(r => setStats(r.data)).finally(() => setLoading(false)); }, []);
  const ingestionData = useMemo(() => (stats?.ingestion_statistics || []).map(s => ({ name: s.source__source_type || "unknown", count: s.count })), [stats]);
  const statusData = useMemo(() => [
    { name: "Approved", value: stats?.approved_records || 0, color: "#059669" },
    { name: "Pending", value: stats?.pending_approvals || 0, color: "#64748b" },
    { name: "Flagged", value: stats?.suspicious_records || 0, color: "#a1a1aa" },
  ], [stats]);
  const cards = [["Total records", stats?.total_records, Database, "slate"], ["Suspicious records", stats?.suspicious_records, AlertTriangle, "amber"], ["Approved records", stats?.approved_records, CheckCircle2, "emerald"], ["Pending approvals", stats?.pending_approvals, Clock3, "zinc"]];

  return <PageLayout title="Dashboard" description="Operational view of ESG ingestion quality, source mix, and approval flow."><div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{cards.map(([label,value,Icon,tone]) => <StatCard key={label} label={label} value={loading ? "-" : value} icon={Icon} tone={tone} />)}</div><div className="mt-6 grid gap-4 xl:grid-cols-[1.4fr_0.9fr]"><Card className="p-5"><div className="flex items-center justify-between gap-4"><div><h2 className="text-base font-semibold text-slate-950">Ingestion by source</h2><p className="mt-1 text-sm text-slate-500">Record volume from connected import streams.</p></div><Badge tone="emerald">Live</Badge></div><div className="mt-5 h-72">{loading ? <div className="h-full animate-pulse rounded-xl bg-slate-100" /> : ingestionData.length ? <ResponsiveContainer width="100%" height="100%"><BarChart data={ingestionData}><CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false}/><XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false}/><YAxis stroke="#64748b" tickLine={false} axisLine={false}/><Tooltip cursor={{ fill: "#f1f5f9" }} contentStyle={{ borderRadius: 12, border: "1px solid #e2e8f0" }}/><Bar dataKey="count" fill="#059669" radius={[8, 8, 0, 0]} /></BarChart></ResponsiveContainer> : <EmptyState title="No ingestion data yet" />}</div></Card><Card className="p-5"><div><h2 className="text-base font-semibold text-slate-950">Approval health</h2><p className="mt-1 text-sm text-slate-500">Current decision status across records.</p></div><div className="mt-5 h-72">{loading ? <div className="h-full animate-pulse rounded-xl bg-slate-100" /> : <ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={statusData} dataKey="value" nameKey="name" innerRadius={62} outerRadius={96} paddingAngle={4}>{statusData.map(entry => <Cell key={entry.name} fill={entry.color} />)}</Pie><Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e2e8f0" }}/></PieChart></ResponsiveContainer>}</div><div className="mt-4 grid gap-2">{statusData.map(item => <div key={item.name} className="flex items-center justify-between rounded-lg bg-slate-50 px-3 py-2 text-sm"><span className="flex items-center gap-2 text-slate-600"><span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.color }} />{item.name}</span><strong className="text-slate-950">{item.value}</strong></div>)}</div></Card></div></PageLayout>;
}
