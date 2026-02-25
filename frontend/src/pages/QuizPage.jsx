import { useEffect, useState, useRef } from "react"
import { useParams } from "react-router-dom"
import API from "../services/api"
import "./quiz.css"
import { Link } from "react-router-dom"

const QuizPage = () => {
  const { quizId } = useParams()

  const [questions, setQuestions] = useState([])
  const [index, setIndex] = useState(0)
  const [selected, setSelected] = useState(null)
  const [score, setScore] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)

  const submittedRef = useRef(false)

  useEffect(() => {
    API.get(`/quiz/${quizId}`)
      .then(res => setQuestions(res.data))
      .catch(console.log)
  }, [quizId])

  const current = questions[index]
  const progress =
    questions.length > 0
      ? ((index + 1) / questions.length) * 100
      : 0

  const submit = () => {
    if (!current || !selected) return

    setShowAnswer(true)

    if (
      selected.toUpperCase() ===
      current.correct_option.toUpperCase()
    ) {
      setScore(prev => prev + 1)
    }

    setTimeout(() => {
      setSelected(null)
      setShowAnswer(false)
      setIndex(prev => prev + 1)
    }, 900)
  }

  useEffect(() => {
    if (
      index >= questions.length &&
      questions.length > 0 &&
      !submittedRef.current
    ) {
      submittedRef.current = true

      API.post(`/quiz/${quizId}/submit`, {
        score,
        total: questions.length
      }).catch(console.log)
    }
  }, [index, questions.length, quizId, score])

  if (index >= questions.length) {
    return (
      <div className="quiz-end">
        <h2>Quiz Completed 🎉</h2>

        <p className="final-score">
          Final Score: <strong>{score}</strong> / {questions.length}
        </p>

        <div className="end-actions">
          <Link to="/dashboard" className="end-btn primary">
            Go to Dashboard
          </Link>

          <Link to={`/quiz/${quizId}`} className="end-btn secondary">
            Retake Quiz
          </Link>
        </div>

      </div>
    )
  }

  return (
    <div className="quiz-page">
      {/* HEADER */}
      <div className="quiz-header">
        <span>
          Question {index + 1} / {questions.length}
        </span>
      </div>

      {/* PROGRESS */}
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* QUESTION CARD */}
      <div className="quiz-card">
        <h3 className="question-text">
          {current.question_text}
        </h3>

        <div className="options">
          {Object.entries(current.options).map(
            ([key, value]) => {
              let className = "option"

              if (showAnswer) {
                if (key === current.correct_option)
                  className += " correct"
                else if (key === selected)
                  className += " wrong"
              } else if (selected === key) {
                className += " selected"
              }

              return (
                <div
                  key={key}
                  className={className}
                  onClick={() =>
                    !showAnswer && setSelected(key)
                  }
                >
                  <strong>{key}.</strong> {value}
                </div>
              )
            }
          )}
        </div>

        <button
          className="next-btn"
          onClick={submit}
          disabled={!selected || showAnswer}
        >
          Next →
        </button>
      </div>
    </div>
  )
}

export default QuizPage