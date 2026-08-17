import axiosInstance from './axiosInstance';

/**
 * Personajga xabar yuboradi va AI javobini qaytaradi.
 */
export async function sendMessage(characterId, message, sessionId) {
  const response = await axiosInstance.post('/chat/send/', {
    character_id: characterId,
    message: message,
    session_id: sessionId,
  });

  return response.data.response;
}