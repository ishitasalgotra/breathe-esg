import { useEffect, useState } from "react";
import api from "../api/client";
import Badge from "../components/Badge";
import PageLayout from "../components/PageLayout";
import Table from "../components/Table";

export default function Suspicious() {
  const [rows, setRows] = useState([]); const [loading, setLoading] = useState(true);
  useEffect(() => { api.get("/emissions/records/suspicious/").then(r => setRows(r.data.results || r.data)).finally(() => setLoading(false)); }, []);
  const columns = [{key:"source_type",label:"Source",render:r=><Badge tone="slate">{r.source_type}</Badge>},{key:"source_row_reference",label:"Row"},{key:"emission_category",label:"Category"},{key:"normalized",label:"Value",render:r=><span className="font-semibold text-slate-900">{r.normalized_value ?? ""} {r.normalized_unit}</span>},{key:"suspicious_reasons",label:"Why flagged",render:r=><div className="max-w-full rounded-lg bg-amber-50 px-3 py-2 text-sm leading-6 text-amber-900">{(r.suspicious_reasons || []).join("; ")}</div>}];
  return <PageLayout title="Suspicious Records" description="Records requiring analyst attention based on validation rules."><div className="mt-6"><Table columns={columns} rows={rows} loading={loading} emptyText="No suspicious records" /></div></PageLayout>;
}
