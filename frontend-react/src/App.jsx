import { useState } from "react";
import "./App.css";

export default function App() {
  const [loginHour, setLoginHour] = useState("");
  const [country, setCountry] = useState("");
  const [device, setDevice] = useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // 🔒 INPUT VALIDATION
  const validateInputs = () => {
  if (loginHour === "" || country === "" || device === "") {
    alert("❌ Please fill all input fields");
    return false;
  }

  if (loginHour < 0 || loginHour > 23) {
    alert("❌ Login hour must be between 0 and 23");
    return false;
  }

  if (!(Number(country) === 0 || Number(country) === 1)) {
    alert("❌ Country must be 0 (Known) or 1 (New)");
    return false;
  }

  if (!(Number(device) === 0 || Number(device) === 1)) {
    alert("❌ Device must be 0 (Known) or 1 (New)");
    return false;
  }

  return true;
};

  const handleSubmit = async () => {
    // 🛑 Stop if invalid
    if (!validateInputs()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "no-cache",
        },
        body: JSON.stringify({
          login_hour: Number(loginHour),
          country: Number(country),
          device: Number(device),
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Backend not reachable. Is FastAPI running?");
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (risk) => {
    if (risk === "HIGH") return "risk-high";
    if (risk === "MEDIUM") return "risk-medium";
    if (risk === "LOW") return "risk-low";
    return "";
  };

  const getActionText = (action) => {
    if (action === "ALLOW") return "✅ Login Allowed";
    if (action === "REQUIRE_OTP") return "🔐 OTP Verification Required";
    if (action === "BLOCK") return "🚫 Login Blocked";
    return action;
  };

  return (
    <div className="wrapper">
      {/* HEADER */}
      <header className="header">
        <h1>🔐 Suspicious Login Detection</h1>
        <p>Simulate a login attempt and analyze its security risk</p>
      </header>

      {/* CARDS */}
      <div className="cards">
        {/* INPUT CARD */}
        <div className="card">
          <label>Login Hour (0–23)</label>
          <input
            type="number"
            min="0"
            max="23"
            value={loginHour}
            onChange={(e) => setLoginHour(e.target.value)}
          />

          <label>Country (0 = Known, 1 = New)</label>
          <input
            type="number"
            min="0"
            max="1"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          />

          <label>Device (0 = Known, 1 = New)</label>
          <input
            type="number"
            min="0"
            max="1"
            value={device}
            onChange={(e) => setDevice(e.target.value)}
          />

          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Login"}
          </button>
        </div>

        {/* RESULT CARD */}
        <div className="card">
          <h2>🧠 Detection Result</h2>

          {!result && (
            <p className="empty">Run analysis to view the decision</p>
          )}

          {result && (
            <div className={`result ${getRiskClass(result.risk_level)}`}>
              <p>
                <strong>Risk Level:</strong>{" "}
                <span className={getRiskClass(result.risk_level)}>
                  {result.risk_level}
                </span>
              </p>

              <p>
                <strong>Action:</strong>{" "}
                <span className="action-text">
                  {getActionText(result.action)}
                </span>
              </p>

              <p>
                <strong>Suspicious:</strong>{" "}
                {result.is_suspicious ? "YES" : "NO"}
              </p>

              <p>
                <strong>Reason:</strong> {result.reason}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
