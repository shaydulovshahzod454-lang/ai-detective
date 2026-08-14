import axiosInstance from './axiosInstance';

export async function getCases() {
  const response = await axiosInstance.get('/cases/');
  return response.data;
}

export async function getCaseDetail(caseId) {
  const response = await axiosInstance.get(`/cases/${caseId}/`);
  return response.data;
}