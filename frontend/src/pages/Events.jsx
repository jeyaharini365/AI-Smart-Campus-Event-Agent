import { useState, useEffect } from "react";
import { CalendarDays, MapPin, Clock, Users, Plus } from "lucide-react";
import api from "../api/axios";
import { isOrganizer } from "../auth";

function Events() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [newEvent, setNewEvent] = useState({
    title: "",
    description: "",
    category: "workshop",
    venue: "",
    start_time: "",
    end_time: "",
    capacity: 50,
  });

  const organizer = isOrganizer();

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await api.get("/events/");
      setEvents(response.data);
    } catch (err) {
      setError("Failed to load events.");
    }
  };

  const handleRegister = async (eventId) => {
    setMessage("");
    setError("");
    try {
      await api.post("/registrations/", {
        event_id: eventId,
        custom_fields_responses: {},
      });
      setMessage("Successfully registered!");
      fetchEvents();
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed.");
    }
  };

  const handlePublish = async (eventId) => {
    setMessage("");
    setError("");
    try {
      await api.put(`/events/${eventId}`, { status: "published" });
      setMessage("Event published!");
      fetchEvents();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to publish event.");
    }
  };

  const handleNewEventChange = (e) => {
    setNewEvent({ ...newEvent, [e.target.name]: e.target.value });
  };

  const handleCreateEvent = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      await api.post("/events/", {
        title: newEvent.title,
        description: newEvent.description,
        category: newEvent.category,
        venue: newEvent.venue,
        start_time: new Date(newEvent.start_time).toISOString(),
        end_time: new Date(newEvent.end_time).toISOString(),
        capacity: Number(newEvent.capacity),
        registration_fields: [],
        faqs: [],
        schedule: [],
      });
      setMessage("Event created successfully!");
      setNewEvent({
        title: "",
        description: "",
        category: "workshop",
        venue: "",
        start_time: "",
        end_time: "",
        capacity: 50,
      });
      setShowForm(false);
      fetchEvents();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create event.");
    }
  };

  return (
    <div className="events-container">
      <h2 style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <CalendarDays size={26} /> Campus Events
      </h2>

      {organizer && (
        <div style={{ marginBottom: "24px" }}>
          <button className="btn-primary" onClick={() => setShowForm(!showForm)} style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "6px" }}>
            <Plus size={18} /> {showForm ? "Cancel" : "Create Event"}
          </button>

          {showForm && (
            <form onSubmit={handleCreateEvent} className="event-card" style={{ marginTop: "16px" }}>
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  name="title"
                  value={newEvent.title}
                  onChange={handleNewEventChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <input
                  type="text"
                  name="description"
                  value={newEvent.description}
                  onChange={handleNewEventChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Category</label>
                <select name="category" value={newEvent.category} onChange={handleNewEventChange}>
                  <option value="workshop">Workshop</option>
                  <option value="seminar">Seminar</option>
                  <option value="cultural">Cultural</option>
                  <option value="sports">Sports</option>
                </select>
              </div>
              <div className="form-group">
                <label>Venue</label>
                <input
                  type="text"
                  name="venue"
                  value={newEvent.venue}
                  onChange={handleNewEventChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Start Time</label>
                <input
                  type="datetime-local"
                  name="start_time"
                  value={newEvent.start_time}
                  onChange={handleNewEventChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>End Time</label>
                <input
                  type="datetime-local"
                  name="end_time"
                  value={newEvent.end_time}
                  onChange={handleNewEventChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Capacity</label>
                <input
                  type="number"
                  name="capacity"
                  value={newEvent.capacity}
                  onChange={handleNewEventChange}
                  required
                />
              </div>
              <button className="btn-primary" type="submit">
                Create Event
              </button>
            </form>
          )}
        </div>
      )}

      {error && <p className="error-text">{error}</p>}
      {message && <p className="success-text">{message}</p>}
      {events.length === 0 && <p>No events found.</p>}
      {events.map((event) => (
        <div key={event._id} className="event-card">
          <h3>{event.title}</h3>
          <p>{event.description}</p>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <MapPin size={16} /> <strong>Venue:</strong> {event.venue}
          </p>
          <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <Clock size={16} /> <strong>When:</strong> {new Date(event.start_time).toLocaleString()}
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
          {organizer && (
            <p style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <Users size={16} /> <strong>Registered:</strong> {event.registered_count} / {event.capacity}
            </p>
          )}
          {!organizer && (
            <button
              className="btn-primary"
              onClick={() => handleRegister(event._id)}
              disabled={event.status !== "published"}
            >
              Register
            </button>
          )}
          {organizer && event.status === "draft" && (
            <button className="btn-primary" onClick={() => handlePublish(event._id)}>
              Publish Event
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default Events;