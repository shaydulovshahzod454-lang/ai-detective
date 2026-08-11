import axios from 'axios';

// Markazlashtirilgan axios nusxasi — barcha API fayllar shundan foydalanadi.
// Bu orqali token bilan bog'liq mantiqni FAQAT bitta joyda yozamiz.
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

// Interceptor — har bir so'rov jo'natilishidan OLDIN ishga tushadi.
// Bu yerda, agar token mavjud bo'lsa, uni so'rov header'iga avtomatik qo'shamiz.
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default axiosInstance;