import { useState } from 'react'
import API from '../services/api'
import './login.css'
import { Link } from 'react-router-dom'
import NavBar from '../components/NavBar'

const Signup = () => {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false);


  const signup = async (e) => {
    e.preventDefault()
    setLoading(true);


    try {
      await API.post('/auth/signup', {
        username,
        email,
        password
      })

      alert("Signup successful")
      window.location.href = '/login'

    } catch (err) {
      console.log(err)
      alert("Signup failed")
    }
    setLoading(false);
  }

  return (

    <div className="login-wrapper">
      <NavBar />
      <div className="login-card">

        {/* LEFT PANEL */}
        <div className="login-left">
          <h1>Heyy!</h1>
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
          <h2>Sign Up</h2>
          <p className="subtitle">
            Register for your quizzes and learning dashboard
          </p>

          <form onSubmit={signup}>

            <input
              placeholder='Username'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />

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
              {loading ? "Registering..." : "Sign Up"}
            </button>
          </form>

          <p className="register-text">
            Already have an account? <span><Link to='/login'>Sign In</Link></span>
          </p>
        </div>

      </div>
    </div>
  )
}

export default Signup
