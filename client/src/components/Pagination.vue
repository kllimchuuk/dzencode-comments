<script setup>
const props = defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
});
const emit = defineEmits(["change"]);

function go(target) {
  if (target >= 1 && target <= props.totalPages) emit("change", target);
}
</script>

<template>
  <nav v-if="totalPages > 1" class="pagination">
    <button type="button" :disabled="page <= 1" @click="go(page - 1)">
      Prev
    </button>
    <span class="pagination-info">Page {{ page }} of {{ totalPages }}</span>
    <button type="button" :disabled="page >= totalPages" @click="go(page + 1)">
      Next
    </button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  justify-content: center;
  margin-top: var(--space-6);
}

.pagination button {
  padding: 0.4rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font: inherit;
  color: var(--text);
  cursor: pointer;
  transition: background 0.15s;
}

.pagination button:hover:not(:disabled) {
  background: var(--bg);
}

.pagination button:disabled {
  color: var(--muted);
  cursor: default;
  opacity: 0.6;
}

.pagination-info {
  color: var(--muted);
  font-size: 0.9rem;
}
</style>
