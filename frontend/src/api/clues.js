import axiosInstance from './axiosInstance';

export async function getClues(caseId, sessionId) {
  const response = await axiosInstance.get('/cases/clues/', {
    params: { case_id: caseId, session_id: sessionId },
  });
  return response.data;
}

export async function addClue(caseId, sessionId, text, sourceCharacterId = null) {
  const response = await axiosInstance.post('/cases/clues/', {
    case_id: caseId,
    session_id: sessionId,
    text: text,
    source_character_id: sourceCharacterId,
  });
  return response.data;
}

export async function deleteClue(clueId) {
  await axiosInstance.delete(`/cases/clues/${clueId}/`);
}