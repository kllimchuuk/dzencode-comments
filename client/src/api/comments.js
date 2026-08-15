import http from "./http";

export async function fetchComments({ ordering, page } = {}) {
  const { data } = await http.get("/comments/", { params: { ordering, page } });
  return data;
}

export async function previewComment(text) {
  const { data } = await http.post("/comments/preview/", { text });
  return data.text;
}
