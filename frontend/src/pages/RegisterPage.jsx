import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser, getCurrentUser } from '../api/auth';
import { useAuth } from '../context/AuthContext';
import './AuthPages.css';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await registerUser(username, password);
      localStorage.setItem('access_token', data.access);
      const userData = await getCurrentUser();
      login(data.access, userData);
      navigate('/');
    } catch (err) {
      console.error(err);
      const message = err.response?.data?.username?.[0] || "Ro'yxatdan o'tishda xatolik.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <h1>Ro'yxatdan o'tish</h1>
      <form onSubmit={handleSubmit}>
        {error && <p className="auth-error">{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Parol (kamida 6 belgi)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Yuborilmoqda...' : "Ro'yxatdan o'tish"}
        </button>
      </form>
      <p className="auth-switch">
        Akkountingiz bormi? <Link to="/login">Kiring</Link>
      </p>
    </div>
  );
}

export default RegisterPage;