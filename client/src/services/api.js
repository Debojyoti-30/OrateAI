import axios from 'axios';
import config from '../config';

const API = axios.create({
  baseURL: config.API_BASE_URL,
});

export const uploadVideo = (formData) =>
  API.post('/video/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
