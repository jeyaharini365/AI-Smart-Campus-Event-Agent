function decodeToken() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch (err) {
    return null;
  }
}

export function getUserRole() {
  const decoded = decodeToken();
  return decoded?.role || null;
}

export function getUserId() {
  const decoded = decodeToken();
  return decoded?.sub || null;
}

export function isOrganizer() {
  return getUserRole() === "organizer";
}