import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import CreateQuiz from './pages/CreateQuiz';
import QuizPage from './pages/QuizPage';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/signup' element={<Signup/>}/>
        <Route path='/dashboard' element={<ProtectedRoute> <Dashboard/> </ProtectedRoute>}/>
        <Route path='/create' element={<ProtectedRoute> <CreateQuiz/> </ProtectedRoute>}/>
        <Route path='/quiz/:quizId' element={<ProtectedRoute> <QuizPage/> </ProtectedRoute>}/>
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;
