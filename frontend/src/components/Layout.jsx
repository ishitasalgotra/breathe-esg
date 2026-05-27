import { Outlet, useNavigate } from "react-router-dom";
import { getCurrentUser } from "../auth";
import Header from "./Header";
import Sidebar from "./Sidebar";

export default function Layout() {
  const navigate = useNavigate();
  const logout = () => { localStorage.clear(); navigate("/login"); };
  const user = getCurrentUser();
  return <div className="min-h-screen lg:flex"><Sidebar user={user} onLogout={logout} /><main className="min-w-0 flex-1"><Header user={user} /><Outlet /></main></div>;
}
