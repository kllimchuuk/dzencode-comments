import { defineStore } from "pinia";
import { ref, computed } from "vue";
import * as authApi from "../api/auth";

export const useAuthStore = defineStore("auth", () => {
  const accessToken = ref(localStorage.getItem("access") || "");
  const refreshToken = ref(localStorage.getItem("refresh") || "");
  const username = ref(localStorage.getItem("username") || "");

  const isAuthenticated = computed(() => !!accessToken.value);

  function setTokens(access, refresh) {
    accessToken.value = access;
    refreshToken.value = refresh;
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
  }

  function clear() {
    accessToken.value = "";
    refreshToken.value = "";
    username.value = "";
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
  }

  async function login(credentials) {
    const data = await authApi.login(credentials);
    setTokens(data.access, data.refresh);
    username.value = credentials.username;
    localStorage.setItem("username", credentials.username);
  }

  async function register(payload) {
    await authApi.register(payload);
    await login({ username: payload.username, password: payload.password });
  }

  async function refreshAccess() {
    const data = await authApi.refresh(refreshToken.value);
    setTokens(data.access, data.refresh ?? refreshToken.value);
    return data.access;
  }

  async function logout() {
    try {
      await authApi.logout(refreshToken.value);
    } finally {
      clear();
    }
  }

  return {
    accessToken,
    refreshToken,
    username,
    isAuthenticated,
    login,
    register,
    refreshAccess,
    logout,
  };
});
