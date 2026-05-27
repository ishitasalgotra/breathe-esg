import { useEffect, useRef, useState } from "react";
import { FileUp, Upload } from "lucide-react";
import api from "../api/client";
import Badge from "../components/Badge";
import Card from "../components/Card";
import PageLayout from "../components/PageLayout";
import Table from "../components/Table";
import { useToast } from "../components/Toast";

export default function UploadCenter() {
  const [sourceType, setSourceType] = useState("sap"); const [file, setFile] = useState(null); const [uploads, setUploads] = useState([]); const [message, setMessage] = useState(""); const [loading, setLoading] = useState(true); const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);
  const { showToast } = useToast();
  const load = () =>
  api
    .get("/api/ingestion/uploads/")
    .then((r) => setUploads(r.data.results || r.data))
    .finally(() => setLoading(false));

useEffect(() => {
  load();
}, []);

const submit = async (e) => {
  e.preventDefault();

  if (!file) {
    showToast("Choose a CSV file before uploading.", "info");
    return;
  }

  const form = new FormData();
  form.append("source_type", sourceType);
  form.append("file", file);

  setMessage("Processing upload...");

  try {
    await api.post("/api/ingestion/uploads/", form);

    setMessage("Upload processed.");
    showToast("Upload processed successfully.", "success");

    setFile(null);

    if (inputRef.current) inputRef.current.value = "";

    load();
  } catch (err) {
    const error =
      err.response?.data?.file?.[0] || "Upload failed.";

    setMessage(error);
    showToast(error, "error");
  }
};
  const onDrop = (e) => { e.preventDefault(); setDragging(false); const nextFile = e.dataTransfer.files?.[0]; if (nextFile) setFile(nextFile); };
  const columns = [{key:"original_filename", label:"File",render:r=><span className="font-medium text-slate-800">{r.original_filename}</span>},{key:"source_type", label:"Source",render:r=><span className="capitalize">{r.source_type}</span>},{key:"upload_status", label:"Status",render:r=><Badge value={r.upload_status} />},{key:"row_count", label:"Rows"},{key:"error_count", label:"Flagged",render:r=><Badge value={r.error_count ? "flagged" : "clear"} />}];
  return <PageLayout title="Upload Center" description="Import CSV data, validate rows, and monitor ingestion results."><Card className="mt-6 p-4 sm:p-5"><form onSubmit={submit} className="grid gap-4 lg:grid-cols-[240px_1fr_auto] lg:items-end"><label className="grid gap-1.5"><span className="text-sm font-semibold text-slate-700">Source type</span><select className="input" value={sourceType} onChange={e=>setSourceType(e.target.value)}><option value="sap">SAP procurement/fuel</option><option value="utility">Utility electricity</option><option value="travel">Corporate travel</option></select></label><div className="grid gap-1.5"><span className="text-sm font-semibold text-slate-700">CSV file</span><label onDragOver={e=>{e.preventDefault(); setDragging(true);}} onDragLeave={()=>setDragging(false)} onDrop={onDrop} className={`flex min-h-24 cursor-pointer items-center justify-center rounded-xl border border-dashed px-4 py-5 text-center transition duration-200 ${dragging ? "border-emerald-400 bg-emerald-50" : "border-slate-300 bg-slate-50 hover:border-emerald-300 hover:bg-emerald-50/60"}`}><input ref={inputRef} className="sr-only" type="file" accept=".csv" onChange={e=>setFile(e.target.files[0])}/><div><FileUp className="mx-auto text-emerald-700" size={24}/><div className="mt-2 text-sm font-semibold text-slate-800">{file ? file.name : "Drop CSV here or browse"}</div><div className="mt-1 text-xs text-slate-500">CSV files only</div></div></label></div><button className="btn-primary"><Upload size={16}/>Upload CSV</button>{message && <div className="rounded-lg bg-slate-50 px-3 py-2 text-sm font-medium text-slate-600 lg:col-span-3">{message}</div>}</form></Card><div className="mt-6"><Table columns={columns} rows={uploads} loading={loading} emptyText="No uploads yet" /></div></PageLayout>;
}
