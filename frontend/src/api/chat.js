import axios from 'axios';

// Backend manzili — hozircha to'g'ridan-to'g'ri yozamiz,
// keyinroq buni .env faylga chiqaramiz
const API_BASE_URL = 'http://127.0.0.1:8000/api/chat';

/**
 * Personajga xabar yuboradi va AI javobini qaytaradi.
 */
export async function sendMessage(characterId, message, sessionId) {
  const response = await axios.post(`${API_BASE_URL}/send/`, {
    character_id: characterId,
    message: message,
    session_id: sessionId,
  });

  return response.data.response;
}