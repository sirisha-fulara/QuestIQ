import { Link } from "react-router-dom"
import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import './navbar.css'

const NavBar = () => {
    const [auth, setAuth] = useState(false);
    const navigate = useNavigate()

    useEffect(() => {
        const token = localStorage.getItem('token')
        setAuth(!!token)
    }, [])

    const logout = () => {
        localStorage.removeItem('token')
        setAuth(false)
        navigate('/')
    }

    return (
        <div className='nav-container'>
            <div className="logo">
                <img src='/logo.png' alt="QuestIQ" />
            </div>
            <div className="right-cont">
                {!auth ? (
                    <>
                        <Link className="nav-item btn" to='/login'>Login</Link>
                        <Link className="nav-item btn" to='/Signup'>Signup</Link>
                    </>
                ) : (
                    <>
                        <Link className="nav-item" to='/create'>Create Quiz</Link>
                        <Link className="nav-item" to='/dashboard'>Dashboard</Link>
                        <button className="btn" onClick={logout}>Logout</button>
                    </>
                )}
            </div>

        </div>
    )
}

export default NavBar
