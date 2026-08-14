import axiosInstance from './axiosInstance';

// ==== Scenes ====
export async function getScenes(caseId) {
  const res = await axiosInstance.get(`/cases/${caseId}/scenes/`);
  return res.data;
}
export async function createScene(caseId, data) {
  const res = await axiosInstance.post(`/cases/${caseId}/scenes/`, data);
  return res.data;
}
export async function updateScene(caseId, sceneId, data) {
  const res = await axiosInstance.patch(`/cases/${caseId}/scenes/${sceneId}/`, data);
  return res.data;
}
export async function deleteScene(caseId, sceneId) {
  await axiosInstance.delete(`/cases/${caseId}/scenes/${sceneId}/`);
}

// ==== Characters ====
export async function getCharacters(caseId) {
  const res = await axiosInstance.get(`/cases/${caseId}/characters/`);
  return res.data;
}
export async function createCharacter(caseId, data) {
  const res = await axiosInstance.post(`/cases/${caseId}/characters/`, data);
  return res.data;
}
export async function updateCharacter(caseId, characterId, data) {
  const res = await axiosInstance.patch(`/cases/${caseId}/characters/${characterId}/`, data);
  return res.data;
}
export async function deleteCharacter(caseId, characterId) {
  await axiosInstance.delete(`/cases/${caseId}/characters/${characterId}/`);
}