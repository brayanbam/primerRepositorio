import axios from "axios";

const apiAnalisis = axios.create({
  baseURL: "http://localhost:5000"
});

apiAnalisis.interceptors.request.use(config => {

  const token = localStorage.getItem("token");

  if (token) {

    config.headers.Authorization = `Bearer ${token}`;

  }

  return config;

});

export default apiAnalisis;