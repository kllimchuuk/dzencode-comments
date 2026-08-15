import http from "./http";

export async function fetchComments({ ordering, page } = {}) {
  const { data } = await http.get("/comments/", { params: { ordering, page } });
  return data;
}

export async function previewComment(text) {
  const { data } = await http.post("/comments/preview/", { text });
  return data.text;
}

function appendOptional(body, key, value) {
  if (value != null && value !== "") body.append(key, value);
}

function buildCommentForm(payload) {
  const body = new FormData();
  body.append("user_name", payload.user_name);
  body.append("email", payload.email);
  body.append("text", payload.text);
  body.append("captcha_token", payload.captcha_token);
  body.append("captcha_answer", payload.captcha_answer);
  appendOptional(body, "home_page", payload.home_page);
  appendOptional(body, "parent", payload.parent);
  appendOptional(body, "file", payload.file);
  return body;
}

export async function createComment(payload) {
  const { data } = await http.post("/comments/", buildCommentForm(payload));
  return data;
}
