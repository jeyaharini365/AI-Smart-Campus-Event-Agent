import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { LogIn } from "lucide-react";
import api from "../api/axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.post("/users/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      navigate("/events");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h2 style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}>
        <LogIn size={26} /> Welcome Back
      </h2>
      {error && <p className="error-text">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
      <p style={{ marginTop: "16px", textAlign: "center", fontSize: "14px", color: "#94a3b8" }}>
        Don't have an account? <Link to="/register" style={{ color: "#38bdf8" }}>Register</Link>
      </p>
    </div>
  );
}

export default Login;