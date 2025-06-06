import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const userMessage = prompt;

    try {
      const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: userMessage }),
      });

      const data = await res.json();
      const assistantReply = data.response || data.error || "No response";

      setHistory((prev) => [
      ...prev,
      { role: "user", content: userMessage },
      { role: "assistant", content: assistantReply },
    ]);
    setPrompt(""); // Clear input
  } catch (err) {
    const errorMsg = "Error: " + err.message;
    setResponse(errorMsg);
    setHistory((prev) => [...prev, { role: "assistant", content: errorMsg }]);
  } finally {
    setLoading(false);
  }
};


 return (
  <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
    <h1>AI Chat</h1>
    
    <form onSubmit={handleSubmit}>
      <textarea
        rows="4"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Ask something..."
        disabled={loading}
        style={{ width: "100%", marginBottom: "1rem" }}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Thinking..." : "Send"}
      </button>
    </form>

    <div style={{ marginTop: "2rem" }}>
      <h2>Conversation</h2>
      {history.map((msg, i) => (
        <div
          key={i}
          style={{
            textAlign: msg.role === "user" ? "right" : "left",
            backgroundColor: msg.role === "user" ? "#59edf7" : "#5af745",
            padding: "0.5rem",
            borderRadius: "8px",
            marginBottom: "0.5rem"
          }}
        >
          <p><strong>{msg.role}:</strong> {msg.content}</p>
        </div>
      ))}
    </div>
  </div>
);
}


export default App;
