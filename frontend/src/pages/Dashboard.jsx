import { useState, useEffect } from "react";
import { LayoutDashboard, MapPin, Clock, Users, BarChart3 } from "lucide-react";
import api from "../api/axios";
import { getUserId } from "../auth";

function Dashboard() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  const myId = getUserId();

  useEffect(() => {
    fetchMyEvents();
  }, []);

  const fetchMyEvents = async () => {
    try {
      const response = await api.get("/events/");
      const myEvents = response.data.filter(
        (event) => event.organizer_id === myId
      );
      setEvents(myEvents);
    } catch (err) {
      setError("Failed to load your events.");
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async (eventId) => {
    setMessage("");
    setError("");
    try {
      await api.put(`/events/${eventId}`, { status: "published" });
      setMessage("Event published!");
      fetchMyEvents();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to publish event.");
    }
  };

  const totalRegistrations = events.reduce(
    (sum, event) => sum + (event.registered_count || 0),
    0
  );

  return (
    <div className="events-container">
      <h2 style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <LayoutDashboard size={26} /> My Organizer Dashboard
      </h2>

      {error && <p className="error-text">{error}</p>}
      {message && <p className="success-text">{message}</p>}
      {loading && <p>Loading your events...</p>}

      {!loading && (
        <div className="event-card" style={{ marginBottom: "24px" }}>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <BarChart3 size={16} /> <strong>Total events created:</strong> {events.length}
          </p>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <Users size={16} /> <strong>Total registrations across all events:</strong>{" "}
            {totalRegistrations}
          </p>
        </div>
      )}

      {!loading && events.length === 0 && (
        <p>You haven't created any events yet.</p>
      )}

      {events.map((event) => (
        <div key={event._id} className="event-card">
          <h3>{event.title}</h3>
          <p>{event.description}</p>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <MapPin size={16} /> <strong>Venue:</strong> {event.venue}
          </p>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <Clock size={16} /> <strong>When:</strong>{" "}
            {new Date(event.start_time).toLocaleString()}
          </p>
          <p>
            <strong>Status:</strong>{" "}
            <span
              className={
                event.status === "published"
                  ? "status-badge"
                  : "status-badge draft"
              }
            >
              {event.status}
            </span>
          </p>
          <p>
            <strong>Capacity:</strong> {event.capacity}
          </p>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <Users size={16} /> <strong>Registered:</strong> {event.registered_count || 0}
          </p>
          {event.status === "draft" && (
            <button
              className="btn-primary"
              onClick={() => handlePublish(event._id)}
            >
              Publish Event
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default Dashboard;