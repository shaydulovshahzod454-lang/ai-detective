import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/reports';

export async function submitReport(caseId, sessionId, accusedName, reasoning) {
  const response = await axios.post(`${API_BASE_URL}/submit/`, {
    case_id: caseId,
    session_id: sessionId,
    accused_character_name: accusedName,
    reasoning: reasoning,
  });
  return response.data;
}