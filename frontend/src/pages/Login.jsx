import { useState } from "react";
import API from "../services/api";
import "./login.css";
import { Link } from "react-router-dom";
import NavBar from "../components/NavBar";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const login = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await API.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/dashboard";
    } catch {
      alert("Invalid email or password");
    }
    setLoading(false);
  };

  return (
    <div className="login-wrapper">
      <NavBar/>
      <div className="login-card">

        {/* LEFT PANEL */}
        <div className="login-left">
          <h1>WELCOME</h1>
          <h2>QuestIQ 🚀</h2>
          <p>
            Create smarter quizzes, track your progress, and
            prepare effectively with AI-powered assessments.
          </p>

          <div className="circle big"></div>
          <div className="circle small"></div>
        </div>

        {/* RIGHT PANEL */}
        <div className="login-right">
          <h2>Sign In</h2>
          <p className="subtitle">
            Access your quizzes and learning dashboard
          </p>

          <form onSubmit={login}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit" disabled={loading}>
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <p className="register-text">
            Don’t have an account? <span><Link to='/signup'>Sign Up</Link></span>
          </p>
        </div>

      </div>
    </div>
  );
};

export default Login;