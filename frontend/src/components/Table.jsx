import EmptyState from "./EmptyState";

export default function Table({ columns, rows, loading, emptyText = "No records found" }) {
  if (loading) {
    return <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-card"><div className="space-y-3">{[0, 1, 2, 3].map(item => <div key={item} className="h-10 animate-pulse rounded-lg bg-slate-100" />)}</div></div>;
  }

  return <div className="rounded-xl border border-slate-200 bg-white shadow-card"><div className="max-h-[62vh] overflow-auto rounded-xl"><table className="w-full min-w-[760px] table-fixed border-separate border-spacing-0 text-left text-sm"><thead className="sticky top-0 z-10"><tr>{columns.map(c => <th key={c.key} className="border-b border-slate-200 bg-slate-50 px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">{c.label}</th>)}</tr></thead><tbody>{rows.length === 0 ? <tr><td colSpan={columns.length}><EmptyState title={emptyText} /></td></tr> : rows.map((row, i) => <tr key={row.id || i} className={`transition duration-200 hover:bg-emerald-50/40 ${row.suspicious_flag ? "bg-amber-50/60" : ""}`}>{columns.map(c => <td key={c.key} className="border-b border-slate-100 px-4 py-3 align-top text-slate-700 last:border-r-0"><div className="min-w-0 break-words">{c.render ? c.render(row) : row[c.key]}</div></td>)}</tr>)}</tbody></table></div></div>;
}
