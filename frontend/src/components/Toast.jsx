import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { CheckCircle2, Info, XCircle } from "lucide-react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const showToast = useCallback((message, type = "info") => {
    const id = crypto.randomUUID();
    setToasts(current => [...current, { id, message, type }]);
    setTimeout(() => setToasts(current => current.filter(toast => toast.id !== id)), 3200);
  }, []);
  const value = useMemo(() => ({ showToast }), [showToast]);
  return <ToastContext.Provider value={value}>{children}<div className="fixed right-4 top-4 z-50 grid w-[calc(100vw-2rem)] max-w-sm gap-2">{toasts.map(toast => <ToastItem key={toast.id} toast={toast} />)}</div></ToastContext.Provider>;
}

function ToastItem({ toast }) {
  const Icon = toast.type === "success" ? CheckCircle2 : toast.type === "error" ? XCircle : Info;
  const tone = toast.type === "success" ? "text-emerald-700" : toast.type === "error" ? "text-rose-700" : "text-slate-700";
  return <div className="flex animate-[fadeIn_180ms_ease-out] items-start gap-3 rounded-xl border border-slate-200 bg-white p-3 text-sm font-medium text-slate-700 shadow-soft"><Icon className={tone} size={18}/><span>{toast.message}</span></div>;
}

export function useToast() {
  const context = useContext(ToastContext);
  return context || { showToast: () => {} };
}
