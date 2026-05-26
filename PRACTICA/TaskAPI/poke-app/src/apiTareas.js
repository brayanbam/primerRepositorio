import axios from "axios";

const apiTareas = axios.create({
  baseURL: "http://localhost:5000"
});

apiTareas.interceptors.request.use(config => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiTareas;