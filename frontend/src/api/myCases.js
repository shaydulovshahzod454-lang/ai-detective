import axiosInstance from './axiosInstance';

export async function getMyCases() {
  const response = await axiosInstance.get('/cases/my/');
  return response.data;
}

export async function createCase(title, description, solution) {
  const response = await axiosInstance.post('/cases/my/', { title, description, solution });
  return response.data;
}

export async function getCaseForEdit(caseId) {
  const response = await axiosInstance.get(`/cases/${caseId}/edit/`);
  return response.data;
}

export async function updateCase(caseId, data) {
  const response = await axiosInstance.patch(`/cases/${caseId}/edit/`, data);
  return response.data;
}

export async function togglePublish(caseId) {
  const response = await axiosInstance.post(`/cases/${caseId}/publish/`);
  return response.data;
}

export async function getCollaborators(caseId) {
  const response = await axiosInstance.get(`/cases/${caseId}/collaborators/`);
  return response.data;
}

export async function addCollaborator(caseId, username) {
  const response = await axiosInstance.post(`/cases/${caseId}/collaborators/`, { username });
  return response.data;
}

export async function removeCollaborator(caseId, collaboratorId) {
  await axiosInstance.delete(`/cases/${caseId}/collaborators/${collaboratorId}/`);
}