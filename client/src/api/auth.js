import http from "./http";

export async function register({ username, email, password }) {
  const { data } = await http.post("/auth/register/", {
    username,
    email,
    password,
  });
  return data;
}

export async function login({ username, password }) {
  const { data } = await http.post("/auth/login/", { username, password });
  return data;
}

export async function refresh(refreshToken) {
  const { data } = await http.post("/auth/refresh/", { refresh: refreshToken });
  return data;
}

export async function logout(refreshToken) {
  await http.post("/auth/logout/", { refresh: refreshToken });
}
