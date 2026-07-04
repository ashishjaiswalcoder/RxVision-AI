import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export async function uploadPrescription(file) {
  const form = new FormData();
  form.append('file', file);
  const { data } = await axios.post(`${API_BASE}/upload`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000,
  });
  return data;
}

export async function getMedicines(query = '') {
  const params = query ? { q: query } : {};
  const { data } = await axios.get(`${API_BASE}/medicines`, { params });
  return data;
}

export async function getPharmacies(lat, lng, radius = 1500) {
  const { data } = await axios.get(`${API_BASE}/pharmacies`, {
    params: { lat, lng, radius }
  });
  return data;
}

export async function submitCorrection(payload) {
  const { data } = await axios.post(`${API_BASE}/corrections`, payload);
  return data;
}

export async function getOcrStatus() {
  const { data } = await axios.get(`${API_BASE}/ocr-status`);
  return data;
}
