import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginUser, getCurrentUser } from '../api/auth';
import { useAuth } from '../context/AuthContext';
import './AuthPages.css';

function LoginPage() {
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
      const data = await loginUser(username, password);
      // Token saqlangach, foydalanuvchi ma'lumotini so'raymiz
      localStorage.setItem('access_token', data.access);
      const userData = await getCurrentUser();
      login(data.access, userData);
      navigate('/');
    } catch (err) {
      console.error(err);
      setError("Username yoki parol noto'g'ri.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <h1>Kirish</h1>
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
          placeholder="Parol"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Kirilmoqda...' : 'Kirish'}
        </button>
      </form>
      <p className="auth-switch">
        Akkountingiz yo'qmi? <Link to="/register">Ro'yxatdan o'ting</Link>
      </p>
    </div>
  );
}

export default LoginPage;