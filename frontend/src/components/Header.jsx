import { useLocation } from "react-router-dom";
import { Bell, ShieldCheck } from "lucide-react";
import Badge from "./Badge";

const titles = {
  "/": "Dashboard",
  "/uploads": "Upload Center",
  "/records": "Emission Records",
  "/suspicious": "Suspicious Records",
  "/approvals": "Approval Queue",
  "/audit": "Audit History",
};

export default function Header({ user }) {
  const location = useLocation();
  return <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/85 backdrop-blur"><div className="flex h-16 items-center justify-between gap-4 px-4 sm:px-6 lg:px-8"><div><div className="text-xs font-semibold uppercase tracking-wide text-emerald-700">ESG Operations</div><div className="text-sm font-medium text-slate-600">{titles[location.pathname] || "Workspace"}</div></div><div className="flex items-center gap-2"><Badge value={user?.role || "user"} tone={user?.role === "auditor" ? "zinc" : "emerald"} className="hidden sm:inline-flex" /><div className="hidden items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 md:flex"><ShieldCheck size={15}/>Secure session</div><button className="grid h-9 w-9 place-items-center rounded-full border border-slate-200 bg-white text-slate-600 shadow-sm transition duration-200 hover:-translate-y-0.5 hover:border-emerald-200 hover:text-emerald-700"><Bell size={17}/></button></div></div></header>;
}
