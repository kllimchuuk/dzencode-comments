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
  gap: 1rem;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
}

.pagination button {
  padding: 0.35rem 0.9rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}

.pagination button:disabled {
  color: #9ca3af;
  cursor: default;
}

.pagination-info {
  color: #6b7280;
  font-size: 0.9rem;
}
</style>
