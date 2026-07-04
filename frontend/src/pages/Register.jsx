import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { UserPlus } from "lucide-react";
import api from "../api/axios";

function Register() {
  const [formData, setFormData] = useState({
    email: "",
    full_name: "",
    role: "student",
    password: "",
    department: "",
    academic_year: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/users/register", {
        email: formData.email,
        full_name: formData.full_name,
        role: formData.role,
        password: formData.password,
        profile: {
          department: formData.department,
          academic_year: Number(formData.academic_year) || 1,
          skills: [],
          interests: [],
        },
      });
      setSuccess("Registration successful! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Registration failed. Please try again."
      );
    }
  };

  return (
    <div className="page-container">
      <h2 style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}>
        <UserPlus size={26} /> Register
      </h2>
      {error && <p className="error-text">{error}</p>}
      {success && <p className="success-text">{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Role</label>
          <select name="role" value={formData.role} onChange={handleChange}>
            <option value="student">Student</option>
            <option value="organizer">Organizer</option>
          </select>
        </div>
        <div className="form-group">
          <label>Department</label>
          <input
            type="text"
            name="department"
            value={formData.department}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Academic Year</label>
          <input
            type="number"
            name="academic_year"
            value={formData.academic_year}
            onChange={handleChange}
          />
        </div>
        <button className="btn-primary" type="submit">
          Register
        </button>
      </form>
    </div>
  );
}

export default Register;