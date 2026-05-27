function decodeJwtPayload(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
  } catch {
    return null;
  }
}

export function saveSession(data) {
  localStorage.setItem("accessToken", data.access);
  localStorage.setItem("refreshToken", data.refresh);
  if (data.user) localStorage.setItem("currentUser", JSON.stringify(data.user));
}

export function getCurrentUser() {
  const stored = localStorage.getItem("currentUser");
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      localStorage.removeItem("currentUser");
    }
  }
  const token = localStorage.getItem("accessToken");
  const payload = token ? decodeJwtPayload(token) : null;
  return payload ? { email: payload.email, role: payload.role, tenant_id: payload.tenant_id } : null;
}

export function hasAnyRole(roles) {
  const user = getCurrentUser();
  return Boolean(user && roles.includes(user.role));
}

export function isAuditor() {
  return getCurrentUser()?.role === "auditor";
}
