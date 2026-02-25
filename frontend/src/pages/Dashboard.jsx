import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import {
  LineChart,
  Line,
  XAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  ResponsiveContainer,
  YAxis
} from "recharts"
import NavBar from "../components/NavBar"
import AvatarSelector from "./AvatarSelection"
import API from "../services/api"
import "./dashboard.css"

const Dashboard = () => {
  const [attempts, setAttempts] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [topicStats, setTopicStats] = useState([])
  const [avatar, setAvatar] = useState("/avatars/avatar1.png")

  useEffect(() => {
    API.get("/quiz/attempts").then(res => setAttempts(res.data))
    API.get("/quiz/analytics").then(res => setAnalytics(res.data))
    API.get("/quiz/topic-analytics").then(res => setTopicStats(res.data))
  }, [])

  const xp = analytics ? analytics.total_attempts * 40 : 0
  const maxXp = 500
  const level = Math.floor(xp / 100) + 1
  const rank =
    level < 5 ? "Novice" :
      level < 10 ? "Explorer" :
        level < 15 ? "Elite" :
          "Master"

  // extract skills from attempted quizzes
  const skillMap = {}
  attempts.forEach(a => {
    const skill = a.topic || a.quiz_title.split(" ")[0]
    skillMap[skill] = (skillMap[skill] || 0) + 1
  })
  const skills = Object.entries(skillMap)

  return (
    <div className="dashboard">
      <NavBar></NavBar>
      <div className="dashboard-layout">

        {/* ================= left column ================= */}
        <div className="left-column">

          {/* user card */}
          <div className="user-card">
            <h3 className="system-title">USER LEVELING SYSTEM</h3>

            <div className="avatar-wrapper">
              <img src={avatar} alt="user" />
            </div>
            <h4 className="username">Sirisha</h4>

            <div className="user-meta">
              <span>Level {level}</span>
              <span>Rank: {rank}</span>
            </div>
            <AvatarSelector selected={avatar} onSelect={setAvatar} />

            <div className="xp-bar">
              <div
                className="xp-fill"
                style={{ width: `${Math.min((xp / maxXp) * 100, 100)}%` }}
              />
            </div>

            <p className="xp-text">
              XP {xp} / {maxXp}
            </p>

            <Link to="/create" className="create-btn full">
              ➕ Create Quiz
            </Link>
          </div>

          {/* skill tracker */}
          <div className="skill-card">
            <h4>Skills Acquired</h4>

            {skills.length === 0 && (
              <p className="skill-empty">No skills yet</p>
            )}

            <ul className="skill-list">
              {skills.map(([skill, count]) => (
                <li key={skill} className="skill-item">
                  <span className="skill-name">{skill}</span>
                  <span className="skill-count">{count} quiz{count > 1 ? "zes" : ""}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* xp */}
          <div className="xp-ring-card">
            <h4>Goal Completion</h4>
            <div
              className="xp-ring"
              style={{
                background: `conic-gradient(#c77dff ${(xp / maxXp) * 360}deg, #2a234f 0)`
              }}
            >
              {Math.floor((xp / maxXp) * 100)}%
            </div>
          </div>

        </div>

        {/* ================= right column ================= */}
        <div className="right-column">

          {/* summary */}
          {analytics && (
            <div className="stats-grid">
              <div className="stat-card">
                <p>Total Attempts</p>
                <h3>{analytics.total_attempts}</h3>
              </div>
              <div className="stat-card">
                <p>Average Score</p>
                <h3>{analytics.average_score}</h3>
              </div>
              <div className="stat-card">
                <p>Accuracy</p>
                <h3>{analytics.average_accuracy}%</h3>
              </div>
            </div>
          )}

          {/* charts */}
          {attempts.length > 0 && (
            <div className="charts-grid">
              <div className="chart-card">
                <h4>Accuracy Trend</h4>
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={attempts.slice().reverse()}>
                    <CartesianGrid stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="date" hide />
                    <YAxis />
                    <Tooltip />
                    <Line
                      dataKey="accuracy"
                      stroke="#c77dff"
                      strokeWidth={3}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card">
                <h4>Score Per Quiz</h4>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={attempts.slice().reverse()}>
                    <CartesianGrid stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="quiz_title" hide />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="score" fill="#9d4edd" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* stats */}
          {topicStats.length > 0 && (
            <div className="chart-card full-width">
              <h4>Topic-wise Accuracy</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={topicStats}>
                  <CartesianGrid stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="topic" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="accuracy" fill="#ffb703" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* history */}
          <div className="history-section">
            <h3>Quiz History</h3>
            {attempts.map((a, i) => (
              <div className="history-card" key={i}>
                <strong>{a.quiz_title}</strong>
                <span className="difficulty">{a.difficulty}</span>
                <p>
                  Score: {a.score}/{a.total} <br />
                  Accuracy: {a.accuracy}% <br />
                  Date: {a.date}
                </p>
              </div>
            ))}
          </div>

        </div>
      </div>
    </div>
  )
}

export default Dashboard