import { Inbox } from "lucide-react";

export default function EmptyState({ title = "No records found", message = "Try adjusting your filters or upload new source data." }) {
  return <div className="grid place-items-center px-4 py-12 text-center"><div className="grid h-12 w-12 place-items-center rounded-xl bg-slate-100 text-slate-500"><Inbox size={22} /></div><div className="mt-3 text-sm font-semibold text-slate-900">{title}</div><p className="mt-1 max-w-sm text-sm text-slate-500">{message}</p></div>;
}
