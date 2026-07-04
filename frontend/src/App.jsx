import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import { CalendarDays, MessageCircle, LayoutDashboard, LogOut, LogIn, UserPlus } from "lucide-react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Events from "./pages/Events";
import Chat from "./pages/Chat";
import Dashboard from "./pages/Dashboard";
import { isOrganizer } from "./auth";

function Navbar() {
  const isLoggedIn = !!localStorage.getItem("token");
  const organizer = isOrganizer();

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <nav className="navbar">
      <Link to="/events" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
        <CalendarDays size={18} /> Events
      </Link>
      <Link to="/chat" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
        <MessageCircle size={18} /> Chat
      </Link>
      {isLoggedIn && organizer && (
        <Link to="/dashboard" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <LayoutDashboard size={18} /> Dashboard
        </Link>
      )}
      {!isLoggedIn && (
        <Link to="/login" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <LogIn size={18} /> Login
        </Link>
      )}
      {!isLoggedIn && (
        <Link to="/register" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <UserPlus size={18} /> Register
        </Link>
      )}
      {isLoggedIn && (
        <button onClick={handleLogout} style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <LogOut size={16} /> Logout
        </button>
      )}
    </nav>
  );
}

function PrivateRoute({ children }) {
  const isLoggedIn = !!localStorage.getItem("token");
  return isLoggedIn ? children : <Navigate to="/login" />;
}

function OrganizerRoute({ children }) {
  const isLoggedIn = !!localStorage.getItem("token");
  if (!isLoggedIn) return <Navigate to="/login" />;
  if (!isOrganizer()) return <Navigate to="/events" />;
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/events"
          element={
            <PrivateRoute>
              <Events />
            </PrivateRoute>
          }
        />
        <Route
          path="/chat"
          element={
            <PrivateRoute>
              <Chat />
            </PrivateRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <OrganizerRoute>
              <Dashboard />
            </OrganizerRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;