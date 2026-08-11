import { createContext, useContext, useState, useEffect } from 'react';
import { getCurrentUser } from '../api/auth';

// Context — bu React'da ma'lumotni "chuqur joylashgan" komponentlarga
// har safar props orqali uzatmasdan, to'g'ridan-to'g'ri ulashish usuli.
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkAuth() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (err) {
        // Token eskirgan yoki noto'g'ri — tozalaymiz
        localStorage.removeItem('access_token');
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, []);

  function login(token, userData) {
    localStorage.setItem('access_token', token);
    setUser(userData);
  }

  function logout() {
    localStorage.removeItem('access_token');
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Boshqa komponentlarda "useAuth()" deb chaqirish uchun qulay funksiya
export function useAuth() {
  return useContext(AuthContext);
}