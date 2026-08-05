import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/cases';

export async function getClues(caseId, sessionId) {
  const response = await axios.get(`${API_BASE_URL}/clues/`, {
    params: { case_id: caseId, session_id: sessionId },
  });
  return response.data;
}

export async function addClue(caseId, sessionId, text, sourceCharacterId = null) {
  const response = await axios.post(`${API_BASE_URL}/clues/`, {
    case_id: caseId,
    session_id: sessionId,
    text: text,
    source_character_id: sourceCharacterId,
  });
  return response.data;
}

export async function deleteClue(clueId) {
  await axios.delete(`${API_BASE_URL}/clues/${clueId}/`);
}