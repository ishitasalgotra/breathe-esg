import { Search } from "lucide-react";
export default function Toolbar({ search, setSearch, children }) {
  return <div className="mb-4 flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-3 shadow-card sm:flex-row sm:items-center sm:justify-between"><label className="relative max-w-md flex-1"><Search className="absolute left-3 top-2.5 text-slate-400" size={17}/><input className="input pl-9" value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search records" /></label><div className="flex flex-wrap gap-2">{children}</div></div>;
}
