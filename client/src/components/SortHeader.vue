<script setup>
const props = defineProps({ ordering: { type: String, required: true } });
const emit = defineEmits(["change"]);

const columns = [
  { field: "user_name", label: "User Name" },
  { field: "email", label: "E-mail" },
  { field: "created_at", label: "Date" },
];

function sortBy(field) {
  const asc = props.ordering === field;
  emit("change", asc ? `-${field}` : field);
}

function indicator(field) {
  if (props.ordering === field) return "▲";
  if (props.ordering === `-${field}`) return "▼";
  return "";
}
</script>

<template>
  <div class="sort-header">
    <button
      v-for="col in columns"
      :key="col.field"
      type="button"
      class="sort-col"
      @click="sortBy(col.field)"
    >
      {{ col.label }} <span class="sort-arrow">{{ indicator(col.field) }}</span>
    </button>
  </div>
</template>

<style scoped>
.sort-header {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e2e4e8;
}

.sort-col {
  padding: 0;
  border: none;
  background: none;
  font: inherit;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
}

.sort-arrow {
  color: #2563eb;
}
</style>
