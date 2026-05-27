import { useState } from "react";
import { Activity } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { saveSession } from "../auth";
import Card from "../components/Card";
import { useToast } from "../components/Toast";

export default function Login() {
  const [email, setEmail] = useState("analyst@example.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { showToast } = useToast();
  const submit = async (e) => {
  e.preventDefault();
  setError("");

  try {
    const { data } = await api.post("/api/auth/login/", {
      email,
      password,
    });

    saveSession(data);
    showToast("Signed in successfully.", "success");
    navigate("/");
  } catch (err) {
    const message = "Login failed. Check credentials and backend availability.";
    setError(message);
    showToast(message, "error");
    console.error(err);
  }
};
  return <div className="grid min-h-screen place-items-center px-4"><Card className="w-full max-w-sm p-6"><form onSubmit={submit}><div className="flex items-center gap-3"><div className="grid h-11 w-11 place-items-center rounded-xl bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100"><Activity size={22} /></div><div><h1 className="text-xl font-semibold tracking-tight text-slate-950">Breathe ESG</h1><p className="text-sm text-slate-500">Analyst workspace</p></div></div><div className="mt-6 grid gap-3"><input className="input" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/><input className="input" type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password"/>{error && <div className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700">{error}</div>}<button className="btn-primary w-full" type="submit">Sign in</button></div></form></Card></div>;
}
