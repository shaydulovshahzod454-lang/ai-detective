// ESKI:
// import axios from 'axios';
// const API_BASE_URL = 'http://127.0.0.1:8000/api/cases';

// YANGI:
import axiosInstance from './axiosInstance';

/**
 * Barcha faol case'lar ro'yxatini oladi.
 */
export async function getCases() {
  const response = await axiosInstance.get(`${API_BASE_URL}/`);
  return response.data;
}

/**
 * Bitta case haqida to'liq ma'lumot (scene'lar, character'lar bilan) oladi.
 */
export async function getCaseDetail(caseId) {
  const response = await axiosInstance.get(`${API_BASE_URL}/${caseId}/`);
  return response.data;
}