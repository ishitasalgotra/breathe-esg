import { useEffect, useState } from "react";
import { Check, X } from "lucide-react";
import api from "../api/client";
import Badge from "../components/Badge";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import PageLayout from "../components/PageLayout";
import { useToast } from "../components/Toast";

export default function Approvals() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  const { showToast } = useToast();

  const load = () =>
    api
      .get("/api/approvals/queue/")
      .then((r) => setRows(r.data.results || r.data))
      .finally(() => setLoading(false));

  useEffect(() => {
    load();
  }, []);

  const decide = async (id, status) => {
    await api.post(`/api/approvals/records/${id}/decision/`, {
      status,
      note:
        status === "approved"
          ? "Approved by analyst"
          : "Rejected by analyst",
    });

    showToast(
      status === "approved"
        ? "Record approved."
        : "Record rejected.",
      status === "approved" ? "success" : "info"
    );

    load();
  };

  return (
    <PageLayout
      title="Approval Queue"
      description="Resolve pending emission records and capture analyst decisions."
    >
      <div className="mt-6 grid gap-3">
        {loading ? (
          [0, 1, 2].map((item) => (
            <Card key={item} className="p-5">
              <div className="h-20 animate-pulse rounded-xl bg-slate-100" />
            </Card>
          ))
        ) : rows.length === 0 ? (
          <Card>
            <EmptyState
              title="No pending records"
              message="Approved and rejected records will continue to appear in audit history."
            />
          </Card>
        ) : (
          rows.map((r) => (
            <Card
              key={r.id}
              className="p-4 hover:-translate-y-0.5 hover:shadow-soft sm:p-5"
            >
              <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <div className="font-semibold text-slate-950">
                      {r.emission_category}
                    </div>

                    <Badge tone="slate">
                      {r.source_type}
                    </Badge>

                    {r.suspicious_flag && (
                      <Badge value="flagged" />
                    )}
                  </div>

                  <div className="mt-2 text-sm text-slate-500">
                    {r.source_row_reference} -{" "}
                    <span className="font-semibold text-slate-800">
                      {r.normalized_value} {r.normalized_unit}
                    </span>
                  </div>

                  {r.suspicious_flag && (
                    <div className="mt-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm font-medium leading-6 text-amber-900">
                      {r.suspicious_reasons.join("; ")}
                    </div>
                  )}
                </div>

                <div className="flex shrink-0 flex-wrap gap-2">
                  <button
                    onClick={() => decide(r.id, "approved")}
                    className="btn-primary"
                  >
                    <Check size={16} />
                    Approve
                  </button>

                  <button
                    onClick={() => decide(r.id, "rejected")}
                    className="btn-danger"
                  >
                    <X size={16} />
                    Reject
                  </button>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </PageLayout>
  );
}
