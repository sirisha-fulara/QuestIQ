import NavBar from "../components/NavBar"
import { Link } from "react-router-dom"
import './home.css'

const Home = () => {
  return (
    <div>
      <NavBar></NavBar>
      <div className="home-container">
        <div className="text">
          <p className="heading">Challenge Your Knowledge</p>
          <p className="p1">Challenge yourself by generating the quiz of the topic of your choice in minutes and know your analytics</p>
          <Link className='btn' to='/login'>Let's play</Link>
        </div>
        <div className="img">
          <img  className='home-img' src="/home_img.png" alt="img" />
        </div>
      </div>
    </div>
  )
}

export default Home
