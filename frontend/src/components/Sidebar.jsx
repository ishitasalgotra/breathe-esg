import { NavLink } from "react-router-dom";
import { Activity, AlertTriangle, CheckSquare, Database, History, LayoutDashboard, LogOut, Upload } from "lucide-react";
import Badge from "./Badge";

const nav = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/uploads", label: "Upload Center", icon: Upload, roles: ["admin", "analyst"] },
  { to: "/records", label: "Emission Records", icon: Database },
  { to: "/suspicious", label: "Suspicious Records", icon: AlertTriangle },
  { to: "/approvals", label: "Approval Queue", icon: CheckSquare, roles: ["admin", "analyst"] },
  { to: "/audit", label: "Audit History", icon: History },
];

export default function Sidebar({ user, onLogout }) {
  const visibleNav = nav.filter(item => !item.roles || item.roles.includes(user?.role));
  return <aside className="border-b border-slate-200 bg-white/95 shadow-sm backdrop-blur lg:sticky lg:top-0 lg:flex lg:h-screen lg:w-72 lg:flex-col lg:border-b-0 lg:border-r"><div className="border-b border-slate-200 px-5 py-5"><div className="flex items-center gap-3"><div className="grid h-10 w-10 place-items-center rounded-xl bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100"><Activity size={22} /></div><div><div className="font-semibold tracking-tight text-slate-950">Breathe ESG</div><div className="text-xs font-medium text-slate-500">Ingestion command center</div></div></div><div className="mt-4 flex items-center justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2"><div className="min-w-0 text-xs font-medium text-slate-500"><div className="truncate text-slate-700">{user?.email || "Signed in"}</div><div>Role</div></div><Badge value={user?.role || "user"} tone={user?.role === "auditor" ? "zinc" : "emerald"} /></div></div><nav className="grid gap-1.5 p-3 lg:flex-1">{visibleNav.map(({to,label,icon:Icon}) => <NavLink key={to} to={to} className={({isActive}) => `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition duration-200 ${isActive ? "bg-emerald-50 text-emerald-700 shadow-sm ring-1 ring-emerald-100" : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"}`}><Icon className="transition duration-200 group-hover:scale-105" size={18}/><span>{label}</span></NavLink>)}</nav><button onClick={onLogout} className="m-3 flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition duration-200 hover:bg-rose-50 hover:text-rose-700"><LogOut size={18}/>Log out</button></aside>;
}
