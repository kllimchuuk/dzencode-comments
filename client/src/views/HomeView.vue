<script setup>
import { onMounted } from "vue";
import { useCommentsStore } from "../stores/comments";
import { useCommentSocket } from "../composables/useCommentSocket";
import CommentForm from "../components/CommentForm.vue";
import SortHeader from "../components/SortHeader.vue";
import CommentNode from "../components/CommentNode.vue";
import Pagination from "../components/Pagination.vue";

const store = useCommentsStore();

onMounted(() => store.load());
useCommentSocket();
</script>

<template>
  <section>
    <h2 class="section-title">Add a comment</h2>
    <CommentForm />

    <div class="list-head">
      <h2 class="section-title">Comments</h2>
      <span class="count">{{ store.total }}</span>
    </div>
    <SortHeader :ordering="store.ordering" @change="store.setOrdering" />

    <p v-if="store.loading" class="state">Loading…</p>
    <p v-else-if="!store.roots.length" class="state">No comments yet.</p>
    <div v-else class="comment-list">
      <CommentNode v-for="root in store.roots" :key="root.id" :comment="root" />
    </div>

    <Pagination
      :page="store.page"
      :total-pages="store.totalPages"
      @change="store.setPage"
    />
  </section>
</template>

<style scoped>
.section-title {
  font-size: 1.05rem;
  font-weight: 600;
}

.list-head {
  display: flex;
  gap: var(--space-2);
  align-items: baseline;
  margin-top: var(--space-6);
}

.count {
  padding: 0.05rem 0.5rem;
  background: var(--border);
  border-radius: 999px;
  font-size: 0.8rem;
  color: var(--muted);
}

.state {
  padding: var(--space-4) 0;
  color: var(--muted);
}
</style>
