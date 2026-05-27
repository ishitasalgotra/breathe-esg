import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import UploadCenter from "./pages/UploadCenter.jsx";
import Records from "./pages/Records.jsx";
import Suspicious from "./pages/Suspicious.jsx";
import Approvals from "./pages/Approvals.jsx";
import Audit from "./pages/Audit.jsx";
import { ToastProvider } from "./components/Toast.jsx";
import { hasAnyRole } from "./auth";

function Protected({ children }) { return localStorage.getItem("accessToken") ? children : <Navigate to="/login" replace />; }
function RoleRoute({ roles, children }) { return hasAnyRole(roles) ? children : <Navigate to="/" replace />; }

export default function App() {
  return <ToastProvider><Routes><Route path="/login" element={<Login />} /><Route element={<Protected><Layout /></Protected>}><Route index element={<Dashboard />} /><Route path="uploads" element={<RoleRoute roles={["admin", "analyst"]}><UploadCenter /></RoleRoute>} /><Route path="records" element={<Records />} /><Route path="suspicious" element={<Suspicious />} /><Route path="approvals" element={<RoleRoute roles={["admin", "analyst"]}><Approvals /></RoleRoute>} /><Route path="audit" element={<Audit />} /></Route></Routes></ToastProvider>;
}
