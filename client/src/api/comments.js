import http from "./http";

export async function fetchComments({ ordering, page } = {}) {
  const { data } = await http.get("/comments/", { params: { ordering, page } });
  return data;
}
