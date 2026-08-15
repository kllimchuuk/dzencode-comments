import http from "./http";

export async function fetchCaptcha() {
  const { data } = await http.get("/captcha/");
  return data;
}
