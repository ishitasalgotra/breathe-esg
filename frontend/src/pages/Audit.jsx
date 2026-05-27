import { useEffect, useState } from "react";
import api from "../api/client";
import Badge from "../components/Badge";
import PageLayout from "../components/PageLayout";
import Table from "../components/Table";

function JsonBlock({ value }) {
  return (
    <pre className="max-h-40 max-w-full overflow-auto whitespace-pre-wrap break-words rounded-lg bg-zinc-100 px-3 py-2 text-xs leading-5 text-zinc-700">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

export default function Audit() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/api/audit/")
      .then((r) => setRows(r.data.results || r.data))
      .finally(() => setLoading(false));
  }, []);

  const columns = [
    {
      key: "timestamp",
      label: "Time",
      render: (r) => new Date(r.timestamp).toLocaleString(),
    },
    {
      key: "changed_by_email",
      label: "User",
      render: (r) => (
        <span className="font-medium text-slate-800">
          {r.changed_by_email}
        </span>
      ),
    },
    { key: "entity_type", label: "Entity" },
    { key: "entity_id", label: "ID" },
    {
      key: "action",
      label: "Action",
      render: (r) => <Badge value={r.action} />,
    },
    {
      key: "before_value",
      label: "Before",
      render: (r) => <JsonBlock value={r.before_value} />,
    },
    {
      key: "after_value",
      label: "After",
      render: (r) => <JsonBlock value={r.after_value} />,
    },
  ];

  return (
    <PageLayout
      title="Audit History"
      description="Trace decision, ingestion, and record changes across the workspace."
    >
      <div className="mt-6">
        <Table
          columns={columns}
          rows={rows}
          loading={loading}
          emptyText="No audit events yet"
        />
      </div>
    </PageLayout>
  );
}
