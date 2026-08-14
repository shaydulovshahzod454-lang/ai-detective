import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
  const { user, logout, loading } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/');
  }

  if (loading) return null; // hali auth holatini tekshirayotganda hech narsa ko'rsatmaymiz

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">🔍 AI Detective</Link>

      <div className="navbar-links">
        {user ? (
          <>
            <Link to="/my-cases">Mening case'larim</Link>
            <span className="navbar-username">{user.username}</span>
            <button onClick={handleLogout}>Chiqish</button>
          </>
        ) : (
          <>
            <Link to="/login">Kirish</Link>
            <Link to="/register">Ro'yxatdan o'tish</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;