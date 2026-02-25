import API from "../services/api"
import { useNavigate } from "react-router-dom"
import { useState } from "react"
import NavBar from "../components/NavBar"
import './create.css'

const CreateQuiz = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const createQuiz = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const res = await API.post('/quiz/generate', {
        title: e.target.title.value,
        topic: e.target.topic.value,
        difficulty: e.target.difficulty.value
      })

      navigate(`/quiz/${res.data.quiz_id}`)
    } catch (err) {
      setError("Something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-quiz-container">
      <NavBar />

      <div className="create-form">
        <form onSubmit={createQuiz}>
          <h2>Create Your AI Quiz</h2>

          <p className="quiz-instructions">
            <strong>Set up your quiz in seconds.</strong><br />
            Give your quiz a title, choose a topic, and select difficulty.
          </p>

          <div className="divider"></div>

          <input name="title" placeholder="Quiz Title" required />
          <input name="topic" placeholder="Topic (e.g. Python Loops)" required />

          <select name="difficulty">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          {/* ❌ Error message */}
          {error && <p className="error-msg">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? <span className="loader"></span> : "Create & Start"}
          </button>

          <p className="quiz-footer">
            ✓ Quiz generated instantly • ✓ Start answering immediately
          </p>
        </form>
      </div>
    </div>
  )
}

export default CreateQuiz