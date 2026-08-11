// ESKI:
// import axios from 'axios';
// const API_BASE_URL = 'http://127.0.0.1:8000/api/cases';

// YANGI:
import axiosInstance from './axiosInstance';

/**
 * Personajga xabar yuboradi va AI javobini qaytaradi.
 */
export async function sendMessage(characterId, message, sessionId) {
  const response = await axiosInstance.post(`${API_BASE_URL}/send/`, {
    character_id: characterId,
    message: message,
    session_id: sessionId,
  });

  return response.data.response;
}