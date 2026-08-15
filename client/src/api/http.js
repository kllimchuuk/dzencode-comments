import axios from "axios";
import { useAuthStore } from "../stores/auth";

const http = axios.create({
  baseURL: "/api",
});

function attachToken(config) {
  const auth = useAuthStore();
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
}

function shouldRefresh(error) {
  const auth = useAuthStore();
  return (
    error.response?.status === 401 &&
    !error.config._retry &&
    !error.config.url?.includes("/auth/") &&
    !!auth.refreshToken
  );
}

async function retryWithRefresh(error) {
  const auth = useAuthStore();
  error.config._retry = true;
  try {
    await auth.refreshAccess();
  } catch {
    auth.logout();
    throw error;
  }
  return http(error.config);
}

function onResponseError(error) {
  if (shouldRefresh(error)) {
    return retryWithRefresh(error);
  }
  return Promise.reject(error);
}

http.interceptors.request.use(attachToken);
http.interceptors.response.use((response) => response, onResponseError);

export default http;
