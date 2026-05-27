import { useEffect, useState } from "react";
import api from "../api/client";
import Badge from "../components/Badge";
import PageLayout from "../components/PageLayout";
import Table from "../components/Table";
import Toolbar from "../components/Toolbar";

export default function Records() {
  const [rows, setRows] = useState([]); const [search, setSearch] = useState(""); const [loading, setLoading] = useState(true);
  useEffect(() => { setLoading(true); api.get("/emissions/records/", { params: { search } }).then(r => setRows(r.data.results || r.data)).finally(() => setLoading(false)); }, [search]);
  const columns = [{key:"source_type",label:"Source",render:r=><span className="font-medium capitalize text-slate-800">{r.source_type}</span>},{key:"scope_category",label:"Scope",render:r=><Badge tone="slate">{r.scope_category}</Badge>},{key:"emission_category",label:"Category"},{key:"raw",label:"Raw",render:r=>`${r.raw_value ?? ""} ${r.raw_unit}`},{key:"normalized",label:"Normalized",render:r=><span className="font-semibold text-slate-900">{r.normalized_value ?? ""} {r.normalized_unit}</span>},{key:"approval_status",label:"Approval",render:r=><Badge value={r.approval_status} />},{key:"suspicious_flag",label:"Flagged",render:r=><Badge value={r.suspicious_flag} />}];
  return <PageLayout title="Emission Records" description="Search and review normalized emissions data from connected source files."><div className="mt-6"><Toolbar search={search} setSearch={setSearch}/><Table columns={columns} rows={rows} loading={loading}/></div></PageLayout>;
}
