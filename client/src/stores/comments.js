import { defineStore } from "pinia";
import { ref } from "vue";
import { fetchComments } from "../api/comments";

export const useCommentsStore = defineStore("comments", () => {
  const roots = ref([]);
  const page = ref(1);
  const totalPages = ref(1);
  const total = ref(0);
  const ordering = ref("-created_at");
  const loading = ref(false);

  async function load() {
    loading.value = true;
    try {
      const data = await fetchComments({
        ordering: ordering.value,
        page: page.value,
      });
      roots.value = data.results;
      page.value = data.page;
      totalPages.value = data.total_pages;
      total.value = data.total;
    } finally {
      loading.value = false;
    }
  }

  function setOrdering(value) {
    ordering.value = value;
    page.value = 1;
    return load();
  }

  function setPage(value) {
    page.value = value;
    return load();
  }

  return {
    roots,
    page,
    totalPages,
    total,
    ordering,
    loading,
    load,
    setOrdering,
    setPage,
  };
});
