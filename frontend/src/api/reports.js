import axiosInstance from './axiosInstance';

export async function submitReport(caseId, sessionId, accusedName, reasoning) {
  const response = await axiosInstance.post('/reports/submit/', {
    case_id: caseId,
    session_id: sessionId,
    accused_character_name: accusedName,
    reasoning: reasoning,
  });
  return response.data;
}