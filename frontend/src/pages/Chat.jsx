import { useState } from "react";
import { Bot, Send } from "lucide-react";
import api from "../api/axios";

function Chat() {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [error, setError] = useState("");

  const handleSend = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    const userMessage = message;
    setChatLog((prev) => [...prev, { sender: "You", text: userMessage }]);
    setMessage("");
    setError("");

    try {
      const response = await api.post("/chat/", { message: userMessage });
      setChatLog((prev) => [
        ...prev,
        { sender: "Agent", text: response.data.reply },
      ]);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to get a response.");
    }
  };

  return (
    <div className="chat-container">
      <h2 style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <Bot size={26} /> Campus Event Assistant
      </h2>
      <div className="chat-box">
        {chatLog.length === 0 && (
          <p style={{ color: "#64748b" }}>
            Try asking: "What events are happening?" or "Show my registered events"
          </p>
        )}
        {chatLog.map((entry, idx) => (
          <div
            key={idx}
            className={
              entry.sender === "Agent" ? "chat-message agent" : "chat-message"
            }
          >
            <span className="sender">{entry.sender}:</span>
            <p>{entry.text}</p>
          </div>
        ))}
      </div>
      {error && <p className="error-text">{error}</p>}
      <form onSubmit={handleSend} className="chat-input-row">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <Send size={16} /> Send
        </button>
      </form>
    </div>
  );
}

export default Chat;