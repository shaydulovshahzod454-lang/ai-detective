import axiosInstance from './axiosInstance';

export async function registerUser(username, password) {
  const response = await axiosInstance.post('/accounts/register/', { username, password });
  return response.data;   // { user, access }
}

export async function loginUser(username, password) {
  const response = await axiosInstance.post('/accounts/login/', { username, password });
  return response.data;   // { access, refresh }
}

export async function getCurrentUser() {
  const response = await axiosInstance.get('/accounts/me/');
  return response.data;   // { id, username }
}